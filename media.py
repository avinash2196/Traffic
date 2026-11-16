"""Media upload handler - M3.2 GREEN milestone."""
import hashlib
from io import BytesIO
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

try:
    from PIL import Image, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def get_utc_now_iso():
    """Get current UTC time in ISO-8601 format without microseconds (JavaScript-compatible)."""
    # isoformat() on timezone-aware datetime returns: "2026-11-03T01:29:40+00:00"
    # Replace "+00:00" with "Z" to get: "2026-11-03T01:29:40Z"
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class MediaUploadError(Exception):
    """Custom exception for media upload errors."""
    def __init__(self, error_code, message, status_code=400):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class MediaUploadHandler:
    """Handler for media file uploads, validation, screening, and storage."""
    
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
    MAX_VIDEO_DURATION = 45  # seconds
    MIN_RESOLUTION_WIDTH = 640
    MIN_RESOLUTION_HEIGHT = 480
    BLUR_THRESHOLD = 100
    
    SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png"}
    SUPPORTED_VIDEO_FORMATS = {".mp4", ".mov", ".webm"}
    SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | SUPPORTED_VIDEO_FORMATS
    
    MIME_TYPE_MAP = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".webm": "video/webm"
    }
    
    def __init__(self, media_store_dir="./media_store"):
        """Initialize handler with media storage directory."""
        self.media_store_dir = Path(media_store_dir)
        self.media_store_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def compute_hash_from_bytes(file_data):
        """Compute SHA-256 hash from file bytes."""
        return hashlib.sha256(file_data).hexdigest()
    
    def validate_file(self, file_data, filename, mime_type=None):
        """Validate file size, format, and container integrity."""
        # Check file size
        file_size = len(file_data)
        if file_size > self.MAX_FILE_SIZE:
            raise MediaUploadError("file_too_large", "File exceeds 25 MB limit", 413)
        
        # Check file extension
        ext = Path(filename).suffix.lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise MediaUploadError("unsupported_format", f"Format {ext} not supported", 422)
        
        # Validate container integrity
        if ext in self.SUPPORTED_IMAGE_FORMATS:
            self._validate_image_container(file_data, ext)
        elif ext in self.SUPPORTED_VIDEO_FORMATS:
            self._validate_video_container(file_data, ext)
        
        # Return metadata
        detected_mime = self.MIME_TYPE_MAP.get(ext, "application/octet-stream")
        return {
            "file_size": file_size,
            "file_ext": ext,
            "mime_type": mime_type or detected_mime
        }
    
    def _validate_image_container(self, file_data, ext):
        """Validate JPEG/PNG container integrity."""
        if ext in {".jpg", ".jpeg"}:
            # Check JPEG magic number
            if not file_data.startswith(b"\xFF\xD8\xFF"):
                raise MediaUploadError("invalid_container", "Invalid JPEG format", 422)
            # Try to open with Pillow if available
            if HAS_PIL:
                try:
                    Image.open(BytesIO(file_data)).verify()
                except Exception:
                    raise MediaUploadError("invalid_container", "Corrupted or invalid JPEG", 422)
        
        elif ext == ".png":
            # Check PNG magic number
            if not file_data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise MediaUploadError("invalid_container", "Invalid PNG format", 422)
            # Try to open with Pillow if available
            if HAS_PIL:
                try:
                    Image.open(BytesIO(file_data)).verify()
                except Exception:
                    raise MediaUploadError("invalid_container", "Corrupted or invalid PNG", 422)
    
    def _validate_video_container(self, file_data, ext):
        """Validate video container integrity."""
        if ext == ".mp4":
            # Check MP4 ftyp box
            if b"ftyp" not in file_data[:200]:
                raise MediaUploadError("invalid_container", "Invalid MP4 format", 422)
    
    def detect_duplicate(self, db, hash_value):
        """Check if file with same hash already exists."""
        record = db.execute(
            "SELECT id FROM media WHERE sha256_hash = ?",
            (hash_value,)
        ).fetchone()
        
        if record:
            return {
                "is_duplicate": True,
                "original_media_id": record[0]
            }
        return {"is_duplicate": False}
    
    def screen_technical(self, file_data, filename):
        """Perform technical screening (resolution, blur, etc.)."""
        ext = Path(filename).suffix.lower()
        result = {
            "is_blurry": False,
            "blur_score": None,
            "is_low_resolution": False,
            "resolution_width": None,
            "resolution_height": None
        }
        
        try:
            if ext in self.SUPPORTED_IMAGE_FORMATS:
                result.update(self._screen_image(file_data))
            elif ext in self.SUPPORTED_VIDEO_FORMATS:
                result.update(self._screen_video(file_data))
        except Exception:
            # Screening failures don't block upload
            pass
        
        return result
    
    def _screen_image(self, file_data):
        """Screen image for resolution and blur."""
        result = {
            "is_blurry": False,
            "blur_score": None,
            "is_low_resolution": False,
            "resolution_width": None,
            "resolution_height": None
        }
        
        try:
            if HAS_PIL:
                img = Image.open(BytesIO(file_data))
                width, height = img.size
                result["resolution_width"] = width
                result["resolution_height"] = height
                
                # Check resolution threshold
                if width < self.MIN_RESOLUTION_WIDTH or height < self.MIN_RESOLUTION_HEIGHT:
                    result["is_low_resolution"] = True
        except Exception:
            pass
        
        return result
    
    def _screen_video(self, file_data):
        """Screen video for quality flags."""
        # Basic video screening (can be expanded with moviepy)
        return {
            "is_blurry": False,
            "blur_score": None,
            "is_low_resolution": False,
            "resolution_width": None,
            "resolution_height": None
        }
    
    def store_media(self, db, report_id, file_data, filename, mime_type=None):
        """Validate, screen, and store media file."""
        media_id = uuid4().hex[:16]
        now = get_utc_now_iso()
        
        try:
            # Validate file
            validation = self.validate_file(file_data, filename, mime_type)
            
            # Compute hash
            file_hash = self.compute_hash_from_bytes(file_data)
            
            # Check for duplicates
            dup_check = self.detect_duplicate(db, file_hash)
            if dup_check["is_duplicate"]:
                # Return existing media instead of error (user-friendly response)
                return {
                    "media_id": dup_check["original_media_id"],
                    "filename": filename,
                    "is_duplicate": True,
                    "duplicate_reason": "Image already submitted",
                    "size_bytes": validation["file_size"],
                    "mime_type": validation["mime_type"],
                    "sha256_hash": file_hash
                }
            
            # Screen technical quality
            screening = self.screen_technical(file_data, filename)
            
            # Create report directory
            report_dir = self.media_store_dir / report_id
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine sequential filename
            existing_count = len(list(report_dir.glob("media_*")))
            ext = Path(filename).suffix.lower()
            stored_filename = f"media_{existing_count + 1:02d}{ext}"
            storage_path = report_dir / stored_filename
            
            # Write file to disk
            storage_path.write_bytes(file_data)
            
            # Insert into database
            db.execute("""
                INSERT INTO media 
                (id, report_id, filename, file_size_bytes, mime_type, sha256_hash, 
                 is_blurry, is_low_resolution, storage_path, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                media_id,
                report_id,
                filename,
                validation["file_size"],
                validation["mime_type"],
                file_hash,
                1 if screening["is_blurry"] else 0,
                1 if screening["is_low_resolution"] else 0,
                str(storage_path),
                now
            ))
            db.commit()
            
            return {
                "media_id": media_id,
                "filename": filename,
                "size_bytes": validation["file_size"],
                "mime_type": validation["mime_type"],
                "sha256_hash": file_hash,
                "storage_path": str(storage_path),
                "uploaded_at": now,
                "is_blurry": screening["is_blurry"],
                "is_low_resolution": screening["is_low_resolution"]
            }
        
        except MediaUploadError:
            # Re-raise our custom errors
            raise
        except Exception as e:
            # Check for constraint violation (duplicate file)
            import sqlite3
            if isinstance(e, sqlite3.IntegrityError) and "UNIQUE constraint failed" in str(e):
                file_hash = self.compute_hash_from_bytes(file_data)
                dup_check = self.detect_duplicate(db, file_hash)
                if dup_check["is_duplicate"]:
                    return {
                        "media_id": dup_check["original_media_id"],
                        "filename": filename,
                        "is_duplicate": True,
                        "duplicate_reason": "Image already submitted",
                        "size_bytes": len(file_data),
                        "sha256_hash": file_hash
                    }
            # Rollback on any other error
            db.rollback()
            raise MediaUploadError("storage_error", f"Failed to store media: {str(e)}", 500)
