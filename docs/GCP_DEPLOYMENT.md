# RoadWatch GCP Deployment Guide

**Production deployment on Google Cloud Platform**

---

## 📋 Prerequisites

- **GCP Account** with billing enabled
- **gcloud CLI** installed (`gcloud --version`)
- **Docker** installed locally (for building image)
- **`LOCAL_DEPLOYMENT.md`** completed (tested locally first)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  Cloud Load Balancer (HTTPS)                    │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  Cloud Run (Serverless Container)              │
│  - App replicas: 2–10 (auto-scaling)            │
│  - Memory: 512 MB per instance                  │
│  - Timeout: 3600s                               │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  Cloud Storage (Media)                          │
│  - Bucket: roadwatch-media-{PROJECT_ID}         │
│  - CORS enabled for direct upload               │
└──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  Cloud SQL (PostgreSQL)                         │
│  - Instance: roadwatch-db                       │
│  - Database: roadwatch                          │
│  - User: roadwatch_user                         │
│  - Backups: daily, 30 days retention            │
└──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  Cloud Logging & Monitoring                     │
│  - Application Insights                         │
│  - Error tracking                               │
│  - Performance metrics                          │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Quick Deploy (10 minutes)

### Step 1: Set up GCP project

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

gcloud init
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com \
  compute.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com
```

### Step 3: Create PostgreSQL instance

```bash
gcloud sql instances create roadwatch-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --backup-start-time=03:00 \
  --backup=true \
  --retained-backups-count=30 \
  --enable-bin-log=true
```

### Step 4: Create database & user

```bash
# Connect to instance
gcloud sql connect roadwatch-db --user=postgres

# Run SQL:
CREATE DATABASE roadwatch;
CREATE USER roadwatch_user WITH PASSWORD 'REPLACE_WITH_STRONG_PASSWORD';
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO roadwatch_user;
GRANT ALL ON DATABASE roadwatch TO roadwatch_user;
\q
```

### Step 5: Create Cloud Storage bucket

```bash
gsutil mb -l us-central1 gs://roadwatch-media-$(gcloud config get-value project)

# Enable CORS
gsutil cors set - gs://roadwatch-media-$(gcloud config get-value project) << 'EOF'
[
  {
    "origin": ["*"],
    "method": ["GET", "POST", "DELETE"],
    "responseHeader": ["Content-Type", "Authorization"],
    "maxAgeSeconds": 3600
  }
]
EOF
```

### Step 6: Build & push Docker image

```bash
# Authenticate Docker
gcloud auth configure-docker gcr.io

# Build image
docker build -t gcr.io/$(gcloud config get-value project)/roadwatch:latest .

# Push to Container Registry
docker push gcr.io/$(gcloud config get-value project)/roadwatch:latest
```

### Step 7: Deploy to Cloud Run

```bash
gcloud run deploy roadwatch \
  --image=gcr.io/$(gcloud config get-value project)/roadwatch:latest \
  --platform=managed \
  --region=us-central1 \
  --memory=512Mi \
  --cpu=1 \
  --timeout=3600 \
  --allow-unauthenticated \
  --min-instances=1 \
  --max-instances=10 \
  --set-env-vars=\
ROADWATCH_REVIEWER_TOKEN=REPLACE_WITH_TOKEN,\
OTEL_EXPORTER_OTLP_PROTO_HTTP_ENDPOINT=https://monitoring.googleapis.com:443
```

### Step 8: Update database URL

Get Cloud SQL connection string:
```bash
gcloud sql instances describe roadwatch-db \
  --format='value(connectionName)'
```

Add environment variable:
```bash
gcloud run services update roadwatch \
  --region=us-central1 \
  --update-env-vars=\
DATABASE_URL=postgresql://roadwatch_user:PASSWORD@/roadwatch?host=/cloudsql/PROJECT:us-central1:roadwatch-db
```

### Step 9: Get public URL

```bash
gcloud run services describe roadwatch --region=us-central1 --format='value(status.url)'
```

**Output:** `https://roadwatch-xxx-uc.a.run.app`

---

## 🔐 Environment Variables (GCP)

Set via Cloud Run:

```bash
gcloud run services update roadwatch \
  --region=us-central1 \
  --update-env-vars=\
ROADWATCH_REVIEWER_TOKEN=your-secure-token,\
DATABASE_URL=postgresql://user:pass@/roadwatch?host=/cloudsql/...,\
MEDIA_STORE_PATH=gs://roadwatch-media-project,\
LOG_LEVEL=INFO,\
OPENAI_API_KEY=sk-...,\
OPENAI_MODEL=gpt-4o-mini
```

Or via Cloud Secrets Manager:

```bash
# Create secret
echo -n "your-secret-token" | gcloud secrets create roadwatch-reviewer-token --data-file=-

# Reference in Cloud Run
gcloud run services update roadwatch \
  --region=us-central1 \
  --set-secrets=ROADWATCH_REVIEWER_TOKEN=roadwatch-reviewer-token:latest
```

---

## 📊 Database Migration

### Migrate from SQLite to PostgreSQL

```bash
# Export schema from local SQLite
sqlite3 roadwatch.db ".schema" > schema.sql

# Create Python migration script
python << 'EOF'
import sqlite3
import psycopg2
import json

# Read from SQLite
sqlite_conn = sqlite3.connect('./roadwatch.db')
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# Connect to Cloud SQL (via proxy)
pg_conn = psycopg2.connect(
    "host=/cloudsql/PROJECT:us-central1:roadwatch-db "
    "user=roadwatch_user password=PASSWORD dbname=roadwatch"
)
pg_cursor = pg_conn.cursor()

# Migrate reports
sqlite_cursor.execute("SELECT * FROM reports")
for row in sqlite_cursor.fetchall():
    pg_cursor.execute(
        "INSERT INTO reports VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        "ON CONFLICT (report_id) DO NOTHING",
        tuple(row)
    )

# Migrate media
sqlite_cursor.execute("SELECT * FROM media")
for row in sqlite_cursor.fetchall():
    pg_cursor.execute(
        "INSERT INTO media VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        "ON CONFLICT DO NOTHING",
        tuple(row)
    )

# Migrate events (append-only, safe to duplicate)
sqlite_cursor.execute("SELECT * FROM events")
for row in sqlite_cursor.fetchall():
    pg_cursor.execute(
        "INSERT INTO events VALUES (%s,%s,%s,%s,%s)",
        tuple(row)
    )

pg_conn.commit()
sqlite_conn.close()
pg_conn.close()
print("Migration complete!")
EOF
```

---

## 📁 Cloud Storage Setup

### Media Upload to GCS

Modify `media.py`:

```python
from google.cloud import storage

def save_media_to_gcs(report_id, media_file):
    """Upload media to Google Cloud Storage"""
    bucket_name = os.getenv("MEDIA_BUCKET")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{report_id}/{media_file.filename}")
    blob.upload_from_file(media_file.file)
    return f"gs://{bucket_name}/{report_id}/{media_file.filename}"
```

Or use signed URLs:

```python
# Generate signed URL for direct download
from datetime import timedelta

url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(minutes=15),
    method="GET"
)
```

---

## 🔍 Monitoring & Logs

### View logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=roadwatch" \
  --limit=50 \
  --format=json
```

### Set up alerts

```bash
# Create alert policy for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="RoadWatch High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-filter='resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_count"'
```

### Metrics to monitor
- Request latency (target: <500ms)
- Error rate (target: <1%)
- Container memory (target: <70%)
- Database connections (target: <10)

---

## 🔐 Security Hardening

### 1. Enable IAM roles

```bash
# Restrict Cloud Run access
gcloud run services add-iam-policy-binding roadwatch \
  --region=us-central1 \
  --member=user:admin@example.com \
  --role=roles/run.invoker
```

### 2. Enable VPC connector (Private network)

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create roadwatch-connector \
  --region=us-central1 \
  --subnet=default

# Update Cloud Run
gcloud run services update roadwatch \
  --region=us-central1 \
  --vpc-connector=roadwatch-connector \
  --vpc-egress=all-traffic
```

### 3. Enable Cloud SQL Auth proxy

```bash
# Cloud Run will use Cloud SQL Auth proxy automatically
# Add service account:
gcloud sql instances patch roadwatch-db \
  --database-flags=cloudsql_iam_authentication=on
```

### 4. Rotate secrets

```bash
# Update reviewer token
gcloud secrets versions add roadwatch-reviewer-token \
  --data-file=- <<< "new-token-value"

# Cloud Run automatically uses latest version
```

### 5. Enable HTTP/2 and HTTPS

Cloud Run provides HTTPS by default.

---

## 📊 Costs Estimation

**Monthly costs (light usage):**
- Cloud Run: ~$1–5 (512MB, 1 CPU, 2–10 instances)
- Cloud SQL (db-f1-micro): ~$10
- Cloud Storage: ~$0.50 (media storage)
- Logging: ~$0.50
- **Total: ~$12–16/month**

**Scale-up (production):**
- Cloud Run: ~$50–200 (high traffic)
- Cloud SQL (db-n1-standard-2): ~$50
- Cloud Storage: $5–50 (terabytes)
- Monitoring: ~$10
- **Total: ~$115–310/month**

---

## 🚀 Auto-scaling Configuration

### Cloud Run scaling policy

```bash
gcloud run services update roadwatch \
  --region=us-central1 \
  --min-instances=1 \
  --max-instances=10 \
  --concurrency=80  # Max concurrent requests per instance
```

### Cloud SQL scaling

```bash
# Enable high-availability
gcloud sql instances patch roadwatch-db \
  --backup-location=us \
  --enable-bin-log \
  --replication-type=ASYNCHRONOUS
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy-gcp.yml`:

```yaml
name: Deploy to GCP

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Build and push Docker image
        run: |
          gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/roadwatch:latest
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy roadwatch \
            --image gcr.io/$GCP_PROJECT_ID/roadwatch:latest \
            --region us-central1 \
            --allow-unauthenticated
```

---

## 📈 Scaling for Growth

### Phase 1: MVP (Current)
- Cloud Run: 2 instances, 512MB
- Cloud SQL: db-f1-micro
- ✅ Ready for ~100 users/day

### Phase 2: Growth (100–1000 users/day)
- Cloud Run: 5 instances, 1GB
- Cloud SQL: db-n1-standard-1
- Add Redis: Cloud Memorystore
- Add CDN: Cloud CDN

### Phase 3: Scale (1000+ users/day)
- Cloud Run: 10 instances, 2GB
- Cloud SQL: db-n1-standard-2 (HA)
- Kubernetes Engine (GKE): For custom workloads
- BigTable: For analytics

---

## 🆘 Troubleshooting

### Deploy fails: "Image not found"
```bash
# Ensure image is pushed
docker push gcr.io/$(gcloud config get-value project)/roadwatch:latest

# Verify image exists
gcloud container images list
```

### Database connection fails
```bash
# Check Cloud SQL instance is running
gcloud sql instances describe roadwatch-db

# Verify proxy is configured
gcloud run services describe roadwatch --region=us-central1 --format='value(spec.template.spec.containers[0].env)'
```

### High costs
```bash
# Check Cloud Run invocations
gcloud logging read "resource.type=cloud_run_revision" --format=json | jq '.[] | .httpRequest.status' | sort | uniq -c

# Reduce max instances
gcloud run services update roadwatch --max-instances=5
```

### Slow response time
```bash
# Check CPU/memory usage
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container_memory_utilization"'

# Increase memory
gcloud run services update roadwatch --memory=1Gi
```

---

## ✅ Deployment Checklist

- [ ] GCP project created and APIs enabled
- [ ] Cloud SQL instance running (PostgreSQL)
- [ ] Database and user created
- [ ] Cloud Storage bucket with CORS
- [ ] Docker image built and pushed to GCR
- [ ] Cloud Run service deployed
- [ ] Environment variables set
- [ ] Database migration complete
- [ ] HTTPS/TLS verified
- [ ] Monitoring and logging configured
- [ ] Backups enabled
- [ ] Alerts configured
- [ ] Performance tested (load test)
- [ ] Security audit passed
- [ ] Runbook documented

---

## 📞 Support

### GCP Documentation
- Cloud Run: https://cloud.google.com/run/docs
- Cloud SQL: https://cloud.google.com/sql/docs
- Cloud Storage: https://cloud.google.com/storage/docs

### RoadWatch Docs
- `LOCAL_DEPLOYMENT.md` — Local setup
- `COMPLETION.md` — Project overview
- `Plan.md` — Architecture decisions

---

**Document:** `GCP_DEPLOYMENT.md`  
**Last Updated:** 2026-11-02  
**Version:** 1.0

