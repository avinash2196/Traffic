import sys
from pathlib import Path

# Add parent directory to path to find shared modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import os
from dotenv import load_dotenv
import sqlite3
import time
import logging
import json
import httpx

from shared.durable import JobStore, migrate

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Get database path
DB_PATH = Path(os.getenv("DATABASE_URL", "../roadwatch.db")).resolve()

# AI Gateway configuration
AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://127.0.0.1:9004")
AI_GATEWAY_TOKEN = os.getenv("AI_GATEWAY_TOKEN", "")

class AIWorker:
    def __init__(self):
        self.job_store = JobStore(DB_PATH)
        self.running = True
        self.poll_interval = 5  # seconds
        self.client = httpx.AsyncClient(timeout=30.0)
        
    def init_database(self):
        """Initialize database with AI job schema"""
        try:
            conn = sqlite3.connect(DB_PATH)
            migrate(conn)
            conn.close()
            logger.info("✓ Database initialized")
        except Exception as e:
            logger.error(f"Database init failed: {e}")
            raise
    
    async def process_jobs(self):
        """Poll for pending AI jobs and process them"""
        logger.info("AI Worker started - polling for jobs...")
        
        while self.running:
            try:
                # Query for pending jobs
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                
                pending = conn.execute("""
                    SELECT id, report_id, attempt_count 
                    FROM ai_jobs 
                    WHERE state IN ('pending', 'retry-wait')
                    AND attempt_count < 3
                    AND (next_attempt_at IS NULL OR next_attempt_at <= ?)
                    LIMIT 5
                """, (time.time(),)).fetchall()
                
                conn.close()
                
                if pending:
                    logger.info(f"Found {len(pending)} pending jobs")
                    for job in pending:
                        await self.process_job(job['id'], job['report_id'])
                
                # Wait before next poll
                await asyncio.sleep(self.poll_interval)
                
            except Exception as e:
                logger.error(f"Error processing jobs: {e}")
                await asyncio.sleep(self.poll_interval)
    
    async def process_job(self, job_id: str, report_id: str):
        """Process a single AI analysis job by calling /v1/assessments endpoint."""
        try:
            # Claim the job
            token = self.job_store.claim(job_id, "worker", time.time())
            if not token:
                logger.debug(f"Could not claim job {job_id}")
                return
            
            logger.info(f"Processing job {job_id} for report {report_id}")
            
            # Get report details and media from database
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            
            report = conn.execute(
                "SELECT * FROM reports WHERE id = ?",
                (report_id,)
            ).fetchone()
            
            media_list = conn.execute(
                "SELECT id, mime_type, filename, storage_path FROM media WHERE report_id = ? ORDER BY attachment_position",
                (report_id,)
            ).fetchall()
            
            conn.close()
            
            if not report:
                logger.error(f"Report {report_id} not found")
                self.job_store.fail(token, "EVIDENCE_UNAVAILABLE", False, time.time())
                return
            
            # Build evidence array with base64-encoded media
            evidence = []
            for media in media_list:
                try:
                    # Read media file from disk
                    media_path = Path(media['storage_path'])
                    if not media_path.exists():
                        logger.warning(f"Media file not found: {media_path}")
                        continue
                    
                    with open(media_path, 'rb') as f:
                        media_bytes = f.read()
                    
                    # Base64 encode
                    import base64
                    b64_data = base64.b64encode(media_bytes).decode('utf-8')
                    
                    evidence.append({
                        'media_id': media['id'],
                        'mime_type': media['mime_type'],
                        'data_base64': b64_data
                    })
                except Exception as e:
                    logger.error(f"Error reading media {media['id']}: {e}")
                    continue
            
            if not evidence:
                logger.warning(f"No readable media for report {report_id}")
                self.job_store.fail(token, "EVIDENCE_UNAVAILABLE", False, time.time())
                return
            
            # Build proper /v1/assessments request
            assessment_request = {
                "correlation_id": job_id,
                "attempt_id": job_id,
                "attempt_number": 1,
                "evidence_revision": 1,
                "selection": {
                    "provider": "openai",
                    "request_profile_version": "1.0",
                    "media_profile_version": "1.0"
                },
                "prompt": {
                    "text": f"Assess traffic violation: {report['violation_type']} by vehicle {report['vehicle_number']} at {report['location']}",
                    "version": "1.0",
                    "policy_version": "1.0",
                    "legal_reference_version": "1.0"
                },
                "evidence": evidence
            }
            
            # Call AI Gateway /v1/assessments endpoint
            try:
                headers = {
                    "Authorization": f"Bearer {AI_GATEWAY_TOKEN}" if AI_GATEWAY_TOKEN else "Bearer demo-token"
                }
                
                response = await self.client.post(
                    f"{AI_GATEWAY_URL}/v1/assessments",
                    json=assessment_request,
                    headers=headers,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    assessment_result = response.json()
                    logger.info(f"✓ Job {job_id} assessment complete")
                    
                    # Second call: Break down violations
                    breakdown_request = {
                        "assessment": assessment_result.get('assessment', {}),
                        "evidence": evidence
                    }
                    
                    try:
                        breakdown_response = await self.client.post(
                            f"{AI_GATEWAY_URL}/v1/breakdown",
                            json=breakdown_request,
                            headers=headers,
                            timeout=60.0
                        )
                        
                        if breakdown_response.status_code == 200:
                            breakdown_result = breakdown_response.json()
                            logger.info(f"✓ Job {job_id} breakdown complete: {len(breakdown_result.get('breakdown', {}).get('violations', []))} violations")
                            
                            # Combine both results
                            final_result = {
                                "assessment": assessment_result.get('assessment'),
                                "breakdown": breakdown_result.get('breakdown'),
                                "correlation_id": assessment_result.get('correlation_id'),
                                "assessment_time_ms": assessment_result.get('processing_ms'),
                                "breakdown_time_ms": breakdown_result.get('processing_ms')
                            }
                            
                            # Mark job as success with combined result
                            self.job_store.complete(token, final_result, time.time())
                        else:
                            logger.warning(f"Breakdown returned {breakdown_response.status_code}, storing assessment only")
                            self.job_store.complete(token, assessment_result, time.time())
                            
                    except Exception as e:
                        logger.warning(f"Breakdown failed {e}, storing assessment only")
                        self.job_store.complete(token, assessment_result, time.time())
                else:
                    logger.warning(f"AI Gateway returned {response.status_code}: {response.text}")
                    self.job_store.fail(token, f"GATEWAY_ERROR_{response.status_code}", True, time.time())
                    
            except httpx.TimeoutException:
                logger.warning(f"AI Gateway timeout for job {job_id}")
                self.job_store.fail(token, "REQUEST_TIMEOUT", True, time.time())
            except Exception as e:
                logger.error(f"AI Gateway call failed: {e}")
                self.job_store.fail(token, "GATEWAY_BUSY", True, time.time())
            
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            try:
                self.job_store.fail(token, "GATEWAY_BUSY", True, time.time())
            except:
                pass
    
    async def cleanup(self):
        """Clean up resources"""
        self.running = False
        await self.client.aclose()
        logger.info("AI Worker cleanup complete")
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        logger.info("AI Worker stopped")

async def main():
    worker = AIWorker()
    
    try:
        # Initialize database
        worker.init_database()
        
        # Start processing
        await worker.process_jobs()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await worker.cleanup()
    except Exception as e:
        logger.error(f"Worker error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
