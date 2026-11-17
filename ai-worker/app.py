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
        """Process a single AI analysis job"""
        try:
            # Claim the job
            claim_result = self.job_store.claim(job_id, "worker", time.time())
            if not claim_result:
                logger.debug(f"Could not claim job {job_id}")
                return
            
            logger.info(f"Processing job {job_id} for report {report_id}")
            
            # Get report details from database
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            
            report = conn.execute(
                "SELECT * FROM reports WHERE id = ?",
                (report_id,)
            ).fetchone()
            
            media_list = conn.execute(
                "SELECT id, mime_type, filename FROM media WHERE report_id = ?",
                (report_id,)
            ).fetchall()
            
            conn.close()
            
            if not report:
                logger.error(f"Report {report_id} not found")
                self.job_store.fail(job_id, "report_not_found", time.time())
                return
            
            # Prepare analysis request for AI Gateway
            media_items = [dict(m) for m in media_list] if media_list else []
            
            analysis_request = {
                "report_id": report_id,
                "violation_type": report["violation_type"],
                "vehicle_number": report["vehicle_number"],
                "location": report["location"],
                "media_items": media_items,
                "settings": {"ai_enabled": True}
            }
            
            # Call AI Gateway to analyze
            try:
                response = await self.client.post(
                    f"{AI_GATEWAY_URL}/api/ai/analyze",
                    json=analysis_request,
                    headers={"X-Gateway-Token": AI_GATEWAY_TOKEN} if AI_GATEWAY_TOKEN else {}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✓ Job {job_id} analysis complete: {result.get('status', 'unknown')}")
                    
                    # Mark job as success and store result
                    self.job_store.succeed(
                        job_id,
                        json.dumps(result),
                        time.time()
                    )
                else:
                    logger.warning(f"AI Gateway returned {response.status_code}: {response.text}")
                    self.job_store.retry(job_id, f"gateway_error_{response.status_code}", time.time())
                    
            except httpx.TimeoutException:
                logger.warning(f"AI Gateway timeout for job {job_id}")
                self.job_store.retry(job_id, "gateway_timeout", time.time())
            except Exception as e:
                logger.error(f"AI Gateway call failed: {e}")
                self.job_store.retry(job_id, str(e), time.time())
            
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            try:
                self.job_store.fail(job_id, f"processing_error: {e}", time.time())
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
