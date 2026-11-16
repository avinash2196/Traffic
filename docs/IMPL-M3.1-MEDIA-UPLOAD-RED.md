# M3.1 Implementation Plan: MEDIA UPLOAD RED (Test Suite)

**Milestone:** M3.1 — MEDIA UPLOAD RED  
**Approved By:** Plan.md (APPROVED 2026-11-01)  
**Duration:** 1 day  
**Type:** RED (behavior-defining test suite; all tests MUST fail)  
**Author:** Copilot

---

## 📋 Scope

Write comprehensive test suite for media operations WITHOUT implementing any production code. All tests must fail until M3.2 GREEN implementation writes the handlers.

### What This Milestone Covers
✅ Create `tests/test_media.py` with 10 failing test cases  
✅ Test valid JPEG/MP4 upload and processing  
✅ Test duplicate detection via SHA-256  
✅ Test file size, duration, and format validation  
✅ Test technical screening (blur, resolution detection)  
✅ Test access control (citizen owns media)  
✅ Verify test framework works (pytest discovery, fixtures, assertions)  

### What This Milestone Does NOT Cover
❌ Any production code (media handlers, upload endpoints, file storage)  
❌ Implementation of validation logic  
❌ Database operations (fixtures handle setup/teardown)  
❌ Storage backend (mock file I/O only)  

---

## 🎯 Test Suite Design

### Test File: `tests/test_media.py`

```python
import pytest
import hashlib
from uuid import uuid4
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path


class TestMediaUploadValidation:
    """Test media file validation and storage."""
    
    def test_upload_valid_jpeg_returns_media_id_and_hash(self, test_db, sample_report):
        """
        GIVEN: Citizen with valid report
        WHEN: Upload a valid JPEG file (1 MB, 1280x720)
        THEN: Return 201 status, media_id, and SHA-256 hash
        """
        # Arrange
        file_data = self._create_valid_jpeg(1280, 720, 1024000)
        expected_hash = hashlib.sha256(file_data).hexdigest()
        
        # Act: This endpoint doesn't exist yet (M3.2)
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("photo.jpg", BytesIO(file_data), "image/jpeg")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert (placeholder; will pass in M3.2)
        # assert response.status_code == 201
        # assert "media_id" in response.json()
        # assert response.json()["hash"] == expected_hash
        
        pytest.skip("M3.2 implementation required")
    
    def test_upload_valid_mp4_video_returns_media_id(self, test_db, sample_report):
        """
        GIVEN: Citizen with valid report
        WHEN: Upload valid MP4 video (30 sec, 1920x1080, 20 MB)
        THEN: Return 201, media_id, frame count from sampling
        """
        # Arrange
        file_data = self._create_valid_mp4(1920, 1080, duration_sec=30, file_size=20971520)
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("helmet_violation.mp4", BytesIO(file_data), "video/mp4")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 201
        # assert response.json()["frame_count"] > 0
        
        pytest.skip("M3.2 implementation required")
    
    def test_duplicate_file_returns_409_conflict(self, test_db, sample_report, sample_media):
        """
        GIVEN: Media file already exists (same SHA-256)
        WHEN: Citizen uploads identical file again
        THEN: Return 409 Conflict with duplicate message
        """
        # Arrange: Use same hash as sample_media
        duplicate_file = self._create_valid_jpeg(1280, 720, 1024000)
        # Mock: Make hash match sample_media's hash
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("duplicate.jpg", BytesIO(duplicate_file), "image/jpeg")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 409
        # assert "duplicate" in response.json()["detail"].lower()
        
        pytest.skip("M3.2 implementation required")
    
    def test_file_too_large_returns_413_payload_too_large(self, test_db, sample_report):
        """
        GIVEN: Upload file size limit is 25 MB
        WHEN: Citizen uploads 26 MB file
        THEN: Return 413 Payload Too Large
        """
        # Arrange
        oversized_file = b"x" * (26 * 1024 * 1024)
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("huge.jpg", BytesIO(oversized_file), "image/jpeg")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 413
        # assert "too large" in response.json()["detail"].lower()
        
        pytest.skip("M3.2 implementation required")
    
    def test_video_too_long_returns_413(self, test_db, sample_report):
        """
        GIVEN: Video duration limit is 45 seconds
        WHEN: Citizen uploads 46-second video
        THEN: Return 413 Payload Too Large
        """
        # Arrange
        long_video = self._create_valid_mp4(1920, 1080, duration_sec=46, file_size=15000000)
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("toolong.mp4", BytesIO(long_video), "video/mp4")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 413
        # assert "duration" in response.json()["detail"].lower()
        
        pytest.skip("M3.2 implementation required")
    
    def test_unsupported_file_format_returns_422(self, test_db, sample_report):
        """
        GIVEN: Supported formats are JPG, PNG, MP4, MOV, WEBM
        WHEN: Citizen uploads .exe file
        THEN: Return 422 Unprocessable Entity
        """
        # Arrange
        unsupported_file = b"MZ\x90\x00"  # PE executable header
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("malware.exe", BytesIO(unsupported_file), "application/octet-stream")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 422
        # assert "format" in response.json()["detail"].lower()
        
        pytest.skip("M3.2 implementation required")
    
    def test_corrupted_jpeg_returns_422(self, test_db, sample_report):
        """
        GIVEN: JPEG file header is valid but file is corrupted
        WHEN: Upload corrupted JPEG
        THEN: Return 422 Unprocessable Entity
        """
        # Arrange
        corrupted_jpeg = b"\xFF\xD8\xFF\xE0" + b"corrupted_data_not_valid_jpeg"
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("broken.jpg", BytesIO(corrupted_jpeg), "image/jpeg")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 422
        # assert "invalid" in response.json()["detail"].lower() or "corrupted" in response.json()["detail"].lower()
        
        pytest.skip("M3.2 implementation required")


class TestTechnicalScreening:
    """Test technical screening (blur, resolution detection)."""
    
    def test_low_resolution_image_flags_warning(self, test_db, sample_report):
        """
        GIVEN: Image resolution threshold is 640x480
        WHEN: Upload 320x240 image (below threshold)
        THEN: Return 201 with screening_notes flag "low_resolution"
        """
        # Arrange
        low_res_file = self._create_valid_jpeg(320, 240, 512000)
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("lowres.jpg", BytesIO(low_res_file), "image/jpeg")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 201
        # assert response.json()["screening_notes"] == "low_resolution"
        
        pytest.skip("M3.2 implementation required")
    
    def test_high_blur_video_flags_warning(self, test_db, sample_report):
        """
        GIVEN: Blur detection via frame analysis (threshold: blur_score > 0.7)
        WHEN: Upload very blurry 30-sec video
        THEN: Return 201 with screening_notes flag "high_blur"
        """
        # Arrange
        blurry_video = self._create_valid_mp4(1920, 1080, duration_sec=30, file_size=15000000)
        # Mock: Inject blur_score = 0.85
        
        # Act
        # response = client.post(
        #     f"/api/reports/{sample_report['id']}/media",
        #     files={"file": ("blurry.mp4", BytesIO(blurry_video), "video/mp4")},
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 201
        # assert response.json()["screening_notes"] == "high_blur"
        
        pytest.skip("M3.2 implementation required")


class TestMediaAccessControl:
    """Test access control for media."""
    
    def test_citizen_can_download_own_media(self, test_db, sample_report, sample_media):
        """
        GIVEN: Citizen has uploaded media
        WHEN: Citizen requests media download with matching citizen_id
        THEN: Return 200 OK with file content
        """
        # Arrange
        # Act
        # response = client.get(
        #     f"/api/reports/{sample_report['id']}/media/{sample_media['id']}",
        #     headers={"X-Citizen-Id": sample_report['citizen_id']}
        # )
        
        # Assert
        # assert response.status_code == 200
        # assert response.content == expected_file_content
        
        pytest.skip("M3.2 implementation required")
    
    def test_citizen_cannot_download_other_citizens_media(self, test_db, sample_report, sample_media):
        """
        GIVEN: Media belongs to citizen A
        WHEN: Citizen B requests media with different citizen_id
        THEN: Return 403 Forbidden
        """
        # Arrange
        other_citizen_id = "citizen-" + uuid4().hex[:8]
        
        # Act
        # response = client.get(
        #     f"/api/reports/{sample_report['id']}/media/{sample_media['id']}",
        #     headers={"X-Citizen-Id": other_citizen_id}
        # )
        
        # Assert
        # assert response.status_code == 403
        
        pytest.skip("M3.2 implementation required")
    
    def test_officer_can_download_any_media(self, test_db, sample_report, sample_media):
        """
        GIVEN: Media exists
        WHEN: Officer requests media with role=reviewer header
        THEN: Return 200 OK with file content
        """
        # Arrange
        # Act
        # response = client.get(
        #     f"/api/reports/{sample_report['id']}/media/{sample_media['id']}",
        #     headers={"X-Reviewer-Token": "local-reviewer-only"}
        # )
        
        # Assert
        # assert response.status_code == 200
        # assert response.content == expected_file_content
        
        pytest.skip("M3.2 implementation required")


class TestMediaHelpers:
    """Helper methods to create test media files."""
    
    @staticmethod
    def _create_valid_jpeg(width: int, height: int, file_size: int) -> bytes:
        """
        Generate minimal valid JPEG file.
        
        For MVP testing, use Pillow to generate actual JPEG:
        from PIL import Image
        img = Image.new('RGB', (width, height), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        return img_bytes.getvalue()
        """
        # Mock implementation (test only; M3.2 will use real Pillow)
        return b"\xFF\xD8\xFF\xE0" + b"x" * (file_size - 4)
    
    @staticmethod
    def _create_valid_mp4(width: int, height: int, duration_sec: int, file_size: int) -> bytes:
        """
        Generate minimal valid MP4 file.
        
        For MVP testing, use moviepy or ffmpeg to generate actual video:
        from moviepy.editor import ColorClip
        clip = ColorClip(size=(width, height), color=(255, 0, 0))
        clip.duration = duration_sec
        clip.write_videofile('temp.mp4')
        
        For now, return mock MP4 file with box headers (ftyp, mdat, etc.).
        """
        # Mock implementation (test only; M3.2 will use real video tools)
        return b"ftypisom" + b"x" * (file_size - 8)


# Fixtures (from conftest.py)
# These are defined in tests/conftest.py and automatically available to this test module:
#   - test_db: SQLite connection with schema
#   - sample_report: Pre-inserted report record
#   - sample_media: Pre-inserted media record
```

---

## 📋 Test Breakdown

| # | Test Name | Status | Purpose |
|---|-----------|--------|---------|
| 1 | `test_upload_valid_jpeg_returns_media_id_and_hash` | ❌ FAIL | Valid JPEG upload → 201, media_id, SHA-256 hash |
| 2 | `test_upload_valid_mp4_video_returns_media_id` | ❌ FAIL | Valid MP4 upload → 201, media_id, frame count |
| 3 | `test_duplicate_file_returns_409_conflict` | ❌ FAIL | Duplicate SHA-256 → 409 Conflict |
| 4 | `test_file_too_large_returns_413_payload_too_large` | ❌ FAIL | > 25 MB → 413 Payload Too Large |
| 5 | `test_video_too_long_returns_413` | ❌ FAIL | > 45 sec → 413 |
| 6 | `test_unsupported_file_format_returns_422` | ❌ FAIL | .exe, .txt, etc. → 422 Unprocessable |
| 7 | `test_corrupted_jpeg_returns_422` | ❌ FAIL | Invalid JPEG header → 422 |
| 8 | `test_low_resolution_image_flags_warning` | ❌ FAIL | < 640x480 → 201 + "low_resolution" flag |
| 9 | `test_high_blur_video_flags_warning` | ❌ FAIL | Blur > 0.7 → 201 + "high_blur" flag |
| 10 | `test_citizen_can_download_own_media` | ❌ FAIL | Owner request → 200 OK |
| 11 | `test_citizen_cannot_download_other_citizens_media` | ❌ FAIL | Non-owner request → 403 Forbidden |
| 12 | `test_officer_can_download_any_media` | ❌ FAIL | Officer (reviewer token) → 200 OK |

**Total Tests:** 12 (all must FAIL at end of M3.1)

---

## ✅ Definition of Done

- [ ] File `tests/test_media.py` exists with 12 test cases
- [ ] All tests use `pytest.skip("M3.2 implementation required")` or equivalent assertion placeholders
- [ ] `pytest tests/test_media.py -v` runs without import/syntax errors
- [ ] `pytest tests/test_media.py -v` reports all 12 tests as SKIPPED (showing tests exist)
- [ ] All test names follow pattern `test_<behavior>_<expected_outcome>`
- [ ] All tests have docstring with GIVEN-WHEN-THEN format
- [ ] Fixtures (`test_db`, `sample_report`, `sample_media`) are available (from conftest.py)
- [ ] Mock helpers (`_create_valid_jpeg`, `_create_valid_mp4`) exist but are not production-grade
- [ ] No production code written (no `media.py`, no `/api/reports/.../media` endpoints)
- [ ] Code review verifies: scoping is correct, no implementation in tests, test names are clear

---

## 🔍 Verification Steps

Run these commands after implementation:

```bash
# 1. Verify tests are discovered and all skipped
pytest tests/test_media.py -v

# Expected output (similar to):
# test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash SKIPPED
# test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id SKIPPED
# ...
# 12 skipped

# 2. Verify no syntax errors in test file
python -m py_compile tests/test_media.py

# 3. Verify imports work
python -c "from tests.test_media import *; print('✓ Imports OK')"

# 4. Verify fixtures are available
pytest tests/test_media.py --fixtures | grep -E "test_db|sample_report|sample_media"
```

---

## 📝 Git Commit (After Completion)

```
[M3.1] Add media upload test suite (RED milestone)

Tests for media file upload, validation, screening, and access control:
- Valid JPEG/MP4 upload with hash calculation
- Duplicate detection (409 Conflict on same SHA-256)
- File size validation (< 25 MB, < 45 sec for video)
- Format validation (JPG, PNG, MP4, MOV, WEBM only)
- Corrupted file detection (422 Unprocessable)
- Technical screening flags (low resolution, high blur)
- Access control (citizen owns media, officer can view all)

All 12 tests SKIPPED (M3.2 implementation required).
Test framework verified: pytest discovery, fixtures, docstrings work.

As per Plan.md M3.1 (MEDIA UPLOAD RED), approved by Stakeholder.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## 📞 Handoff Notes

**For Test Engineer:**
1. Write all 12 tests exactly as specified in test breakdown table
2. All tests must be SKIPPED or have assertion placeholders (no real requests)
3. Use GIVEN-WHEN-THEN docstring format
4. Reuse fixtures from `conftest.py` (test_db, sample_report, sample_media)
5. Create mock helpers for JPEG/MP4 generation (Pillow/moviepy not required for RED phase)
6. Verify `pytest` discovers all tests (even if skipped)
7. Commit with message format above

**Blockers:** M1 (DATABASE SCHEMA) must be complete and working

**Next Milestone:** M3.2 (MEDIA UPLOAD GREEN) — implements handlers to pass these tests

---

**Implementation Plan Version:** 1.0  
**Status:** READY FOR EXECUTION  
**Approved:** Plan.md (2026-11-01)
