# IMPL-M3.2-MEDIA-UPLOAD-GREEN.md

**Milestone:** M3.2 (MEDIA UPLOAD GREEN)  
**Type:** GREEN (Implementation to pass RED tests)  
**Duration:** 2 days  
**Dependency:** M3.1 ✅ (12 RED test cases defined)  
**Approval Status:** ⏳ Pending  

---

## 📋 Objective

Implement media upload handlers to pass all 12 RED test cases from M3.1 (`tests/test_media.py`).

---

## 🎯 Deliverables

### 1. Create `media.py` (New File)

File: `C:\Users\avina\Downloads\avinash-repo\v11\Traffic\media.py`

**Contents:**
- `MediaUploadHandler` class with:
  - `validate_file(file_path, max_size, max_duration)` — File validation
  - `compute_hash(file_path)` — SHA-256 hash computation
  - `detect_duplicate(hash_value)` — Lookup in media table
  - `screen_technical(file_path)` — Blur/resolution detection
  - `store_media(report_id, file_obj)` — Save to ./media_store/
  
- Import functions:
  - `from bootstrap import get_db` — Database access
  - `from pathlib import Path` — File operations
  - `import hashlib` — SHA-256
  - `from PIL import Image, ImageFilter` — Blur detection
  - `from moviepy.editor import VideoFileClip` — Video metadata

**Constraints:**
- ✅ No new endpoints (handlers only)
- ✅ No modifications to app.py
- ✅ Use test_db fixture for testing
- ✅ All errors must be explicit (no silent failures)
- ✅ Transactions atomic (commit or rollback)

---

## 📊 RED Test Coverage (M3.1)

All 12 tests in `tests/test_media.py` must PASS:

### Class 1: TestMediaUploadValidation (7 tests)

**1. test_valid_jpeg_upload_25mb_readable**
- GIVEN: Valid 25 MB JPG file, readable JPEG container
- WHEN: Call `MediaUploadHandler.validate_and_store(report_id, file_obj)`
- THEN: 
  - Returns dict with `file_id`, `filename`, `sha256_hash`, `mime_type`, `file_size_bytes`
  - File stored in `./media_store/{report_id}/`
  - Database record created in media table

**2. test_valid_mp4_upload_45sec_readable**
- GIVEN: Valid MP4 file, 45 seconds duration, readable container
- WHEN: Call handler with MP4 file
- THEN:
  - Returns file_id + hash
  - Duration validated (≤ 45 sec)
  - Database record created with duration metadata

**3. test_duplicate_detection_same_file_twice**
- GIVEN: File uploaded once (hash: ABC123), then same file uploaded again
- WHEN: Second upload computes hash
- THEN:
  - Detects duplicate (hash already in media table)
  - Returns error: {"error": "duplicate", "original_media_id": "..."}
  - Does NOT create second media record

**4. test_invalid_container_corrupted_jpeg**
- GIVEN: File with .jpg extension but corrupted/invalid JPEG data
- WHEN: Validation runs
- THEN:
  - Raises ValueError or returns {"error": "invalid_container", "code": "422"}
  - Does NOT store file
  - Does NOT create database record

**5. test_file_too_large_26mb**
- GIVEN: File 26 MB (exceeds 25 MB limit)
- WHEN: Validation runs
- THEN:
  - Raises ValueError or returns {"error": "file_too_large", "code": "413"}
  - Does NOT store file

**6. test_video_too_long_46sec**
- GIVEN: MP4 file with 46 seconds duration (exceeds 45 sec limit)
- WHEN: Duration validation runs
- THEN:
  - Raises ValueError or returns {"error": "video_too_long", "code": "413"}
  - Does NOT store file

**7. test_unsupported_format_exe**
- GIVEN: File with .exe extension or unsupported MIME type
- WHEN: Format validation runs
- THEN:
  - Raises ValueError or returns {"error": "unsupported_format", "code": "422"}
  - Does NOT store file

### Class 2: TestTechnicalScreening (2 tests)

**8. test_low_resolution_flagged_in_metadata**
- GIVEN: JPG with resolution < 640x480 (too low)
- WHEN: Technical screening runs
- THEN:
  - File stored successfully
  - Database record includes `is_low_resolution=True`
  - Metadata available for officer review

**9. test_high_blur_flagged_in_metadata**
- GIVEN: JPG with high blur (Laplacian variance < 100)
- WHEN: Blur detection runs
- THEN:
  - File stored successfully
  - Database record includes `is_blurry=True`
  - Metadata available for officer review

### Class 3: TestMediaAccessControl (3 tests)

**10. test_citizen_can_only_read_own_media**
- GIVEN: Citizen A owns report X with media M1
- WHEN: GET /api/reports/{report_id}/media/{media_id} as citizen B
- THEN:
  - Returns 403 Forbidden
  - Media NOT returned

**11. test_officer_can_read_any_media**
- GIVEN: Officer with reviewer token, any report with media
- WHEN: GET /api/reports/{report_id}/media/{media_id} as officer
- THEN:
  - Returns 200 OK
  - Media file returned (original bytes)

**12. test_media_listing_filtered_by_report**
- GIVEN: Report X with 3 media files
- WHEN: GET /api/reports/{report_id}/media
- THEN:
  - Returns list of 3 media
  - Each has: id, filename, size, hash, upload_time, technical_flags

---

## 🔧 Implementation Details

### File Storage Structure

```
./media_store/
├── {report_id_1}/
│   ├── media_01.jpg       (original file, content hash: SHA256)
│   └── media_02.mp4       (original file)
├── {report_id_2}/
│   └── media_03.jpg       (original file)
```

**Key Points:**
- Directory per report (org by report_id)
- Filename: media_NN.ext (sequential, preserves original extension)
- No subdirectories per media (flat structure per report)
- Storage path stored in database (for later export)

### Database Integration

**Table: media** (already created in M1)
```sql
CREATE TABLE media (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  file_size_bytes INTEGER NOT NULL,
  mime_type TEXT NOT NULL,
  sha256_hash TEXT NOT NULL UNIQUE,
  is_duplicate BOOLEAN DEFAULT 0,
  original_media_id TEXT,  -- If duplicate, reference original
  is_blurry BOOLEAN DEFAULT 0,
  is_low_resolution BOOLEAN DEFAULT 0,
  storage_path TEXT NOT NULL,
  uploaded_at TEXT NOT NULL,
  FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
```

**Constraints:**
- `sha256_hash` is UNIQUE (duplicate detection)
- `is_duplicate` flag for tracking
- `original_media_id` references earlier upload
- All timestamps UTC ISO-8601

### Dependencies to Install

**Already in requirements.txt:**
- Pillow 13.0.0 (for image operations)
- FastAPI 0.162.0
- uvicorn 0.54.0

**May need to add (if not present):**
- moviepy (for video metadata) — Optional; can stub if not available
- hashlib — Standard library (already available)

---

## ✅ Definition of Done

- [ ] media.py created with MediaUploadHandler class
- [ ] All 12 M3.1 RED tests PASS (not SKIPPED)
- [ ] File validation working (size, duration, format, container)
- [ ] Duplicate detection working (SHA-256 hash lookup)
- [ ] Technical screening working (blur, resolution flags)
- [ ] Access control working (citizen isolation, officer override)
- [ ] Storage structure created (/media_store/ with proper permissions)
- [ ] Database records created/updated correctly
- [ ] Transactions atomic (no partial uploads)
- [ ] Error handling explicit (no silent failures)
- [ ] Code passes production code review
- [ ] Commit traceable to this Implementation Plan

---

## 🔍 Verification Steps

### Step 1: Run M3.1 tests
```bash
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic
python -m pytest tests/test_media.py -v
```

**Expected:** All 12 tests PASS (not SKIPPED)

### Step 2: Verify file storage
```bash
ls -la ./media_store/
# Should have subdirectories for each report_id
```

### Step 3: Verify database records
```bash
python -c "
from bootstrap import get_db
db = get_db()
result = db.execute('SELECT COUNT(*) as cnt FROM media').fetchone()
print(f'[OK] Media records in database: {result[0]}')
"
```

### Step 4: Test duplicate detection
```bash
python -c "
# Upload same file twice, verify duplicate flag
# Check: is_duplicate=1, original_media_id set
"
```

### Step 5: Test access control
```bash
python -c "
# Verify citizen A cannot read report B's media
# Verify officer can read all media
"
```

---

## 📝 Implementation Checklist

**Before starting:**
- [ ] M3.1 RED tests reviewed and understood
- [ ] Database schema (media table) reviewed
- [ ] File storage strategy approved (.gitignore updated for ./media_store/)

**During implementation:**
- [ ] media.py created with all required methods
- [ ] Validation logic (size, format, duration) implemented
- [ ] SHA-256 hashing implemented
- [ ] Duplicate detection implemented
- [ ] Technical screening (blur, resolution) implemented
- [ ] File storage (./media_store/) implemented
- [ ] Access control implemented
- [ ] Transactions atomic

**After implementation:**
- [ ] All 12 tests PASS
- [ ] No test failures or errors
- [ ] Storage directory permissions correct
- [ ] Database integrity verified
- [ ] Commit with proper traceability

---

## 🚨 Common Pitfalls to Avoid

1. **Silent failures** — Always raise exceptions; don't return empty dict
2. **Race conditions** — Duplicate hash check must be atomic (check + insert in transaction)
3. **Storage path issues** — Use absolute paths; ensure ./media_store/ writable
4. **Access control bypass** — Verify citizen_id from request scope; don't trust input
5. **Transaction boundaries** — Commit after successful storage; rollback on error
6. **File cleanup on error** — If database insert fails, delete partially stored file

---

## 🔗 Related Documents

- **Plan.md** — M3.2 milestone definition
- **IMPL-M3.1-MEDIA-UPLOAD-RED.md** — RED test specifications (12 test cases)
- **tests/test_media.py** — Actual test code to pass
- **bootstrap.py** — Database functions (init_database, get_db)
- **app.py** — FastAPI entry point (M2)

---

**Approved By:** [Awaiting approval]  
**Approved Date:** [Awaiting approval]  
**Implementation Status:** ⏹️ NOT STARTED

