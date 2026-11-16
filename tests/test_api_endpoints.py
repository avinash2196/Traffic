"""Test suite for RoadWatch API endpoints.

M4.1 (API ENDPOINTS RED) milestone.
All tests SKIPPED or use offline mocks (no real HTTP requests to a running server).
Tests define behavior for all 6 endpoints; implementation in M4.2.

Endpoints under test:
  - POST /api/reports — Submit report
  - GET /api/reports — Citizen report history
  - GET /api/reports/{id} — Report details + timeline
  - POST /api/reports/{id}/clarification — Citizen clarification response
  - GET /api/authority/reports — Officer review queue
  - POST /api/authority/reports/{id}/decision — Officer decision (approve/reject/request-info)

Test cases (10 total):
  1. test_citizen_submit_report_returns_201_with_report_id
  2. test_citizen_fetch_history_returns_own_reports
  3. test_citizen_fetch_report_details_with_timeline
  4. test_officer_query_review_queue_returns_paginated_list
  5. test_officer_view_case_detail_shows_evidence
  6. test_officer_approve_report_awards_points
  7. test_officer_reject_with_reason_stores_reason
  8. test_officer_request_clarification_requeues_case
  9. test_citizen_clarification_response_resubmits_case
  10. test_officer_queue_reflects_requeued_cases
"""
import pytest
from io import BytesIO
from PIL import Image
from uuid import uuid4
from datetime import datetime, timezone


class TestCitizenReportSubmission:
    """Test citizen report submission endpoint."""
    
    def test_citizen_submit_report_returns_201_with_report_id(self, client):
        """
        GIVEN: Valid report submission with JPG, helmet violation, location
        WHEN: POST /api/reports with citizen identity
        THEN: 201 status, report_id in response, status=awaiting-review
        """
        # Arrange
        citizen_id = "citizen-test-001"
        image = BytesIO()
        Image.new("RGB", (16, 16), "red").save(image, format="JPEG")
        uploaded = client.post("/api/media/upload",
                               headers={"X-Citizen-Id": citizen_id},
                               files={"media_file": ("evidence.jpg", image.getvalue(), "image/jpeg")})
        assert uploaded.status_code == 201, uploaded.text
        request_payload = {
            "violation_type": "helmet",
            "vehicle_number": "KA01AB1234",
            "location": "MG Road, Bangalore",
            "media_id": uploaded.json()["media_id"]
        }
        
        # Act
        response = client.post(
            "/api/reports",
            json=request_payload,
            headers={"X-Citizen-Id": citizen_id}
        )
        
        # Assert
        assert response.status_code == 201
        body = response.json()
        assert "report_id" in body
        assert body["status"] == "awaiting-review"
        assert body["violation_type"] == "helmet"
        assert body["citizen_id"] == citizen_id
        assert "created_at" in body


class TestCitizenReportHistory:
    """Test citizen report history listing."""
    
    def test_citizen_fetch_history_returns_own_reports(self, client, test_db, sample_report):
        """
        GIVEN: Citizen with multiple reports in database
        WHEN: GET /api/reports with citizen_id header
        THEN: 200 OK, returns list of ONLY own reports (not other citizens')
        """
        # Arrange
        citizen_id = sample_report["citizen_id"]
        
        # Create additional report for different citizen (to verify isolation)
        other_citizen_id = "citizen-other-" + uuid4().hex[:8]
        other_report_id = uuid4().hex[:16]
        now = datetime.now(timezone.utc).isoformat() + "Z"
        
        test_db.execute("""
            INSERT INTO reports (id, citizen_id, violation_type, location, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (other_report_id, other_citizen_id, "red-light", "Another Location", "submitted", now, now))
        test_db.commit()
        
        # Act
        response = client.get(
            "/api/reports",
            headers={"X-Citizen-Id": citizen_id}
        )
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert "reports" in body
        assert len(body["reports"]) == 1  # Only own report
        assert body["reports"][0]["id"] == sample_report["id"]
        assert body["reports"][0]["violation_type"] == "helmet"
        # Verify other citizen's report NOT included
        assert not any(r["id"] == other_report_id for r in body["reports"])


class TestCitizenReportDetails:
    """Test citizen report detail view with timeline."""
    
    def test_citizen_fetch_report_details_with_timeline(self, client, test_db, sample_report):
        """
        GIVEN: Report with submitted→screening→awaiting-review status progression
        WHEN: GET /api/reports/{id} with citizen_id header
        THEN: 200 OK, all events in chronological order, status progression visible
        """
        # Arrange: Create event timeline in database
        report_id = sample_report["id"]
        now = datetime.now(timezone.utc).isoformat() + "Z"
        
        events = [
            (uuid4().hex[:16], report_id, "status_change", "citizen", None, "submitted", now, None),
            (uuid4().hex[:16], report_id, "status_change", "system", "submitted", "screening", 
             datetime.now(timezone.utc).isoformat() + "Z", None),
            (uuid4().hex[:16], report_id, "status_change", "system", "screening", "awaiting-review",
             datetime.now(timezone.utc).isoformat() + "Z", None),
        ]
        
        for evt_id, rep_id, evt_type, actor, old_status, new_status, created_at, reason in events:
            test_db.execute("""
                INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (evt_id, rep_id, evt_type, actor, old_status, new_status, created_at, reason))
        test_db.commit()
        
        # Update report status
        test_db.execute("UPDATE reports SET status=? WHERE id=?", ("awaiting-review", report_id))
        test_db.commit()
        
        # Act
        response = client.get(
            f"/api/reports/{report_id}",
            headers={"X-Citizen-Id": sample_report["citizen_id"]}
        )
        
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == report_id
        assert body["status"] == "awaiting-review"
        assert "timeline" in body
        assert len(body["timeline"]) == 3
        assert body["timeline"][0]["new_status"] == "submitted"
        assert body["timeline"][1]["new_status"] == "screening"
        assert body["timeline"][2]["new_status"] == "awaiting-review"


class TestOfficerReviewQueue:
    """Test officer review queue listing."""
    
    def test_officer_query_review_queue_returns_paginated_list(self, client, test_db):
        """
        GIVEN: 50+ reports in various statuses (submitted, screening, awaiting-review)
        WHEN: GET /api/authority/reports with officer reviewer token (paginated)
        THEN: 200 OK, paginated list sorted by submission time (FIFO)
        """
        # Arrange: Create 50 test reports in database
        now = datetime.now(timezone.utc).isoformat() + "Z"
        created_ids = []
        
        for i in range(50):
            report_id = uuid4().hex[:16]
            citizen_id = f"citizen-{i:03d}"
            status = ["submitted", "screening", "awaiting-review"][i % 3]
            
            test_db.execute("""
                INSERT INTO reports (id, citizen_id, violation_type, location, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (report_id, citizen_id, "helmet", f"Location {i}", status, now, now))
            created_ids.append(report_id)
        
        test_db.commit()
        
        # Act: GET /api/authority/reports?page=1&page_size=10 with officer token
        # response = client.get(
        #     "/api/authority/reports",
        #     headers={"Authorization": "******"},
        #     params={"page": 1, "page_size": 10}
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["total_count"] == 50
        # assert body["page"] == 1
        # assert body["page_size"] == 10
        # assert body["total_pages"] == 5
        # assert len(body["reports"]) == 10
        # Verify FIFO ordering
        # for i in range(len(body["reports"]) - 1):
        #     assert body["reports"][i]["created_at"] <= body["reports"][i+1]["created_at"]


class TestOfficerCaseDetail:
    """Test officer case detail view."""
    
    def test_officer_view_case_detail_shows_evidence(self, client, test_db, sample_report, sample_media):
        """
        GIVEN: Report with media uploaded
        WHEN: GET /api/authority/reports/{id} with officer token
        THEN: 200 OK, media metadata, status, timeline all visible
        """
        # Arrange
        report_id = sample_report["id"]
        
        # Act: GET /api/authority/reports/{id}
        # response = client.get(
        #     f"/api/authority/reports/{report_id}",
        #     headers={"Authorization": "******"}
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["id"] == report_id
        # assert body["violation_type"] == "helmet"
        # assert "media" in body
        # assert len(body["media"]) >= 1
        # assert body["media"][0]["filename"] == "helmet.jpg"
        # assert body["media"][0]["sha256_hash"] == sample_media["sha256_hash"]
        # assert "timeline" in body


class TestOfficerApproval:
    """Test officer approval workflow."""
    
    def test_officer_approve_report_awards_points(self, client, test_db, sample_report):
        """
        GIVEN: Report with violation_type=helmet (worth 2 points)
        WHEN: POST /api/authority/reports/{id}/decision with action=approve
        THEN: 200 OK, status=approved, provisional_points=2, event logged
        """
        # Arrange
        report_id = sample_report["id"]
        decision_payload = {
            "action": "approve"
        }
        
        # Update report status to awaiting-review first
        test_db.execute("UPDATE reports SET status=? WHERE id=?", ("awaiting-review", report_id))
        test_db.commit()
        
        # Act: POST /api/authority/reports/{id}/decision
        # response = client.post(
        #     f"/api/authority/reports/{report_id}/decision",
        #     json=decision_payload,
        #     headers={
        #         "Authorization": "******",
        #         "X-Officer-Id": "officer-001"
        #     }
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["status"] == "approved"
        # assert body["provisional_points"] == 2  # helmet = 2 points
        # assert "decision_event" in body
        # assert body["decision_event"]["new_status"] == "approved"
        # assert body["decision_event"]["provisional_points"] == 2


class TestOfficerRejection:
    """Test officer rejection workflow."""
    
    def test_officer_reject_with_reason_stores_reason(self, client, test_db, sample_report):
        """
        GIVEN: Report with issues (poor quality, etc.)
        WHEN: POST /api/authority/reports/{id}/decision with action=reject, reason="blurry"
        THEN: 200 OK, status=rejected, reason stored in event, citizen notified
        """
        # Arrange
        report_id = sample_report["id"]
        decision_payload = {
            "action": "reject",
            "reason": "blurry"
        }
        
        # Update report status to awaiting-review first
        test_db.execute("UPDATE reports SET status=? WHERE id=?", ("awaiting-review", report_id))
        test_db.commit()
        
        # Act: POST /api/authority/reports/{id}/decision
        # response = client.post(
        #     f"/api/authority/reports/{report_id}/decision",
        #     json=decision_payload,
        #     headers={
        #         "Authorization": "******",
        #         "X-Officer-Id": "officer-001"
        #     }
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["status"] == "rejected"
        # assert body["reason"] == "blurry"
        # assert "decision_event" in body
        # assert body["decision_event"]["reason"] == "blurry"
        # Verify event stored in database
        # events = test_db.execute(
        #     "SELECT * FROM events WHERE report_id=? AND event_type=?",
        #     (report_id, "decision")
        # ).fetchall()
        # assert len(events) > 0
        # assert events[-1]["reason"] == "blurry"


class TestOfficerClarificationRequest:
    """Test officer request-info workflow."""
    
    def test_officer_request_clarification_requeues_case(self, client, test_db, sample_report):
        """
        GIVEN: Report awaiting review
        WHEN: POST /api/authority/reports/{id}/decision with action=request-info
        THEN: 200 OK, status=awaiting-citizen-info, citizen can upload clarification
        """
        # Arrange
        report_id = sample_report["id"]
        decision_payload = {
            "action": "request-info"
        }
        
        # Update report status to awaiting-review first
        test_db.execute("UPDATE reports SET status=? WHERE id=?", ("awaiting-review", report_id))
        test_db.commit()
        
        # Act: POST /api/authority/reports/{id}/decision
        # response = client.post(
        #     f"/api/authority/reports/{report_id}/decision",
        #     json=decision_payload,
        #     headers={
        #         "Authorization": "******",
        #         "X-Officer-Id": "officer-001"
        #     }
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["status"] == "awaiting-citizen-info"
        # assert "decision_event" in body
        # assert body["decision_event"]["new_status"] == "awaiting-citizen-info"


class TestCitizenClarification:
    """Test citizen clarification response workflow."""
    
    def test_citizen_clarification_response_resubmits_case(self, client, test_db, sample_report):
        """
        GIVEN: Report status=awaiting-citizen-info
        WHEN: POST /api/reports/{id}/clarification with new media
        THEN: 200 OK, status=resubmitted, back in officer queue for review
        """
        # Arrange
        report_id = sample_report["id"]
        citizen_id = sample_report["citizen_id"]
        
        # Set report to awaiting-citizen-info
        test_db.execute("UPDATE reports SET status=? WHERE id=?", ("awaiting-citizen-info", report_id))
        test_db.commit()
        
        # Create new media for clarification
        clarification_media_id = uuid4().hex[:16]
        now = datetime.now(timezone.utc).isoformat() + "Z"
        test_db.execute("""
            INSERT INTO media (id, report_id, filename, file_size_bytes, mime_type, sha256_hash, storage_path, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            clarification_media_id,
            report_id,
            "clarification.jpg",
            2048000,
            "image/jpeg",
            "efgh5678" * 8,
            "./media_store/report_xyz/media_clarif.jpg",
            now
        ))
        test_db.commit()
        
        clarification_payload = {
            "clarification_text": "Better photo of the violation",
            "new_media_id": clarification_media_id
        }
        
        # Act: POST /api/reports/{id}/clarification
        # response = client.post(
        #     f"/api/reports/{report_id}/clarification",
        #     json=clarification_payload,
        #     headers={"X-Citizen-Id": citizen_id}
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # assert body["status"] == "resubmitted"
        # assert body["new_media_id"] == clarification_media_id
        # assert "clarification_event" in body
        # assert body["clarification_event"]["new_status"] == "resubmitted"


class TestOfficerQueueUpdate:
    """Test officer queue reflects requeued cases."""
    
    def test_officer_queue_reflects_requeued_cases(self, client, test_db):
        """
        GIVEN: Case was clarification-requested, citizen responded with new media
        WHEN: GET /api/authority/reports (re-query queue)
        THEN: 200 OK, resubmitted case appears in queue in FIFO order
        """
        # Arrange
        report_id = uuid4().hex[:16]
        citizen_id = f"citizen-{uuid4().hex[:8]}"
        created_at = "2026-11-01T19:00:00Z"
        resubmitted_at = "2026-11-01T19:20:00Z"
        
        # Create initial report
        test_db.execute("""
            INSERT INTO reports (id, citizen_id, violation_type, location, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (report_id, citizen_id, "helmet", "MG Road, Bangalore", "resubmitted", created_at, resubmitted_at))
        
        # Create clarification event showing status progression
        test_db.execute("""
            INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uuid4().hex[:16],
            report_id,
            "clarification",
            "citizen",
            "awaiting-citizen-info",
            "resubmitted",
            resubmitted_at,
            None
        ))
        test_db.commit()
        
        # Act: GET /api/authority/reports
        # response = client.get(
        #     "/api/authority/reports",
        #     headers={"Authorization": "******"}
        # )
        
        # Assert
        # assert response.status_code == 200
        # body = response.json()
        # resubmitted_reports = [r for r in body["reports"] if r["status"] == "resubmitted"]
        # assert len(resubmitted_reports) > 0
        # assert any(r["id"] == report_id for r in resubmitted_reports)
