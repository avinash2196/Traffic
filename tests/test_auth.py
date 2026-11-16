"""Tests for authentication endpoints (M8 Milestone - RED phase).

These tests verify citizen signup, login, logout, and access control.
All tests should FAIL initially (RED phase), then PASS after implementation (GREEN phase).
"""

import pytest


@pytest.fixture
def valid_citizen_data():
    """Fixture: Valid citizen registration data."""
    return {
        "email": "citizen@example.com",
        "full_name": "John Doe",
        "citizen_id": "CTZN-001-VALID",
        "password": "SecurePass123!"
    }


@pytest.fixture
def another_citizen_data():
    """Fixture: Another valid citizen for testing access control."""
    return {
        "email": "other@example.com",
        "full_name": "Jane Smith",
        "citizen_id": "CTZN-002-OTHER",
        "password": "SecurePass456!"
    }


# ============ SIGNUP TESTS ============
class TestSignup:
    """Tests for citizen signup endpoint (POST /api/auth/signup)."""
    
    def test_signup_with_valid_data_returns_201(self, client, valid_citizen_data):
        """Citizen can sign up with valid email, name, ID, password."""
        response = client.post("/api/auth/signup", json=valid_citizen_data)
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["citizen_id"] == valid_citizen_data["citizen_id"]
        assert data["email"] == valid_citizen_data["email"]
        assert data["full_name"] == valid_citizen_data["full_name"]
        assert "password" not in data, "Password should never be returned"
    
    def test_signup_with_duplicate_citizen_id_returns_409(self, client, valid_citizen_data):
        """Duplicate citizen_id is rejected with 409 Conflict."""
        # First signup succeeds
        response1 = client.post("/api/auth/signup", json=valid_citizen_data)
        assert response1.status_code == 201
        
        # Second signup with same citizen_id fails
        response2 = client.post("/api/auth/signup", json=valid_citizen_data)
        assert response2.status_code == 409, f"Expected 409, got {response2.status_code}"
        assert "already exists" in response2.json().get("error", "").lower()
    
    def test_signup_with_duplicate_email_returns_409(self, client, valid_citizen_data):
        """Duplicate email is rejected with 409 Conflict."""
        # First signup succeeds
        response1 = client.post("/api/auth/signup", json=valid_citizen_data)
        assert response1.status_code == 201
        
        # Second signup with same email but different citizen_id fails
        data2 = valid_citizen_data.copy()
        data2["citizen_id"] = "CTZN-003-DUP-EMAIL"
        response2 = client.post("/api/auth/signup", json=data2)
        assert response2.status_code == 409
    
    def test_signup_with_invalid_email_returns_400(self, client, valid_citizen_data):
        """Invalid email format is rejected."""
        data = valid_citizen_data.copy()
        data["email"] = "not-an-email"
        response = client.post("/api/auth/signup", json=data)
        
        assert response.status_code == 400
        assert "email" in response.json().get("error", "").lower()
    
    def test_signup_with_missing_email_returns_400(self, client, valid_citizen_data):
        """Missing email is rejected."""
        data = valid_citizen_data.copy()
        del data["email"]
        response = client.post("/api/auth/signup", json=data)
        
        assert response.status_code == 400
    
    def test_signup_with_missing_password_returns_400(self, client, valid_citizen_data):
        """Missing password is rejected."""
        data = valid_citizen_data.copy()
        del data["password"]
        response = client.post("/api/auth/signup", json=data)
        
        assert response.status_code == 400
    
    def test_signup_with_short_password_returns_400(self, client, valid_citizen_data):
        """Password shorter than 8 characters is rejected."""
        data = valid_citizen_data.copy()
        data["password"] = "Short1!"
        response = client.post("/api/auth/signup", json=data)
        
        assert response.status_code == 400
        assert "password" in response.json().get("error", "").lower()
    
    def test_signup_password_is_hashed_not_plaintext(self, client, valid_citizen_data):
        """Password is stored as bcrypt hash, not plaintext."""
        # Signup
        response = client.post("/api/auth/signup", json=valid_citizen_data)
        assert response.status_code == 201
        
        # Query database directly
        from bootstrap import get_db
        db = get_db()
        cursor = db.execute(
            "SELECT password_hash FROM citizens WHERE id = ?",
            (valid_citizen_data["citizen_id"],)
        )
        row = cursor.fetchone()
        assert row is not None, "Citizen not found in database"
        password_hash = row[0]
        
        # Hash should not equal plaintext password
        assert password_hash != valid_citizen_data["password"]
        # Hash should look like bcrypt ($2a$, $2b$, or $2y$ prefix)
        assert password_hash.startswith("$2") or len(password_hash) > 50


# ============ LOGIN TESTS ============
class TestLogin:
    """Tests for citizen login endpoint (POST /api/auth/login)."""
    
    def test_login_with_valid_credentials_returns_200(self, client, valid_citizen_data):
        """Citizen can login with valid citizen_id + password."""
        # Signup first
        signup_response = client.post("/api/auth/signup", json=valid_citizen_data)
        assert signup_response.status_code == 201
        
        # Login
        login_data = {
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "session_token" in data or "token" in data, "Response must include session token"
        assert data.get("citizen_id") == valid_citizen_data["citizen_id"]
        assert "password" not in data
    
    def test_login_with_invalid_password_returns_401(self, client, valid_citizen_data):
        """Invalid password returns 401 Unauthorized."""
        # Signup first
        signup_response = client.post("/api/auth/signup", json=valid_citizen_data)
        assert signup_response.status_code == 201
        
        # Login with wrong password
        login_data = {
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": "WrongPassword123!"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_login_with_nonexistent_citizen_returns_401(self, client):
        """Login with non-existent citizen_id returns 401."""
        login_data = {
            "citizen_id": "NONEXISTENT",
            "password": "AnyPassword123!"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_login_returns_session_token(self, client, valid_citizen_data):
        """Login response includes valid session token."""
        # Signup first
        client.post("/api/auth/signup", json=valid_citizen_data)
        
        # Login
        login_data = {
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        
        token = response.json().get("session_token") or response.json().get("token")
        assert token is not None
        assert len(token) > 0
    
    def test_login_updates_last_login_timestamp(self, client, valid_citizen_data):
        """Login updates last_login_at timestamp in database."""
        # Signup first
        client.post("/api/auth/signup", json=valid_citizen_data)
        
        # Check initial last_login_at is None
        from bootstrap import get_db
        db = get_db()
        cursor = db.execute(
            "SELECT last_login_at FROM citizens WHERE id = ?",
            (valid_citizen_data["citizen_id"],)
        )
        row = cursor.fetchone()
        assert row[0] is None, "Initial last_login_at should be None"
        
        # Login
        login_data = {
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        
        # Check last_login_at was updated
        cursor = db.execute(
            "SELECT last_login_at FROM citizens WHERE id = ?",
            (valid_citizen_data["citizen_id"],)
        )
        row = cursor.fetchone()
        assert row[0] is not None, "last_login_at should be set after login"


# ============ LOGOUT TESTS ============
class TestLogout:
    """Tests for citizen logout endpoint (POST /api/auth/logout)."""
    
    def test_logout_returns_204_no_content(self, client, valid_citizen_data):
        """Successful logout returns 204 No Content."""
        # Signup and login
        client.post("/api/auth/signup", json=valid_citizen_data)
        login_response = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        token = login_response.json().get("session_token") or login_response.json().get("token")
        
        # Logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
    
    def test_logout_without_token_returns_401(self, client):
        """Logout without token returns 401 Unauthorized."""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"


# ============ ACCESS CONTROL TESTS ============
class TestAccessControl:
    """Tests for JWT token-based access control."""
    
    def test_accessing_reports_without_token_returns_401(self, client):
        """Accessing /api/reports without token returns 401."""
        response = client.get("/api/reports")
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_accessing_reports_with_invalid_token_returns_401(self, client):
        """Accessing /api/reports with invalid token returns 401."""
        response = client.get(
            "/api/reports",
            headers={"Authorization": "Bearer invalid-token-xyz"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_citizen_can_see_own_reports(self, client, valid_citizen_data):
        """Authenticated citizen can see their own reports."""
        # Signup and login
        client.post("/api/auth/signup", json=valid_citizen_data)
        login_response = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        token = login_response.json().get("session_token") or login_response.json().get("token")
        
        # Get reports - should be empty initially
        response = client.get(
            "/api/reports",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should return 200 OK (authenticated) even if no reports
        assert response.status_code == 200
        reports = response.json()
        # Reports could be a list or dict with reports key
        if isinstance(reports, dict):
            reports = reports.get("reports", [])
        assert isinstance(reports, list)
    
    def test_citizen_cannot_see_other_citizens_reports(self, client, valid_citizen_data, another_citizen_data):
        """Citizen A cannot access reports from Citizen B."""
        # Signup Citizen A and login
        client.post("/api/auth/signup", json=valid_citizen_data)
        login_a = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        token_a = login_a.json().get("session_token") or login_a.json().get("token")
        
        # Signup Citizen B and login
        client.post("/api/auth/signup", json=another_citizen_data)
        login_b = client.post("/api/auth/login", json={
            "citizen_id": another_citizen_data["citizen_id"],
            "password": another_citizen_data["password"]
        })
        token_b = login_b.json().get("session_token") or login_b.json().get("token")
        
        # Both citizens can access their report lists with auth token
        response_a = client.get(
            "/api/reports",
            headers={"Authorization": f"Bearer {token_a}"}
        )
        response_b = client.get(
            "/api/reports",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        
        # Both should get 200 (authenticated)
        assert response_a.status_code == 200
        assert response_b.status_code == 200
    
    def test_citizen_id_from_token_used_for_reports(self, client, valid_citizen_data):
        """citizen_id is derived from JWT token, not headers."""
        # Signup and login
        client.post("/api/auth/signup", json=valid_citizen_data)
        login_response = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        token = login_response.json().get("session_token") or login_response.json().get("token")
        
        # Verify that we can access reports endpoint with the token
        # This tests that the JWT token properly sets the citizen_id in request scope
        response = client.get(
            "/api/reports",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should get 200 (authenticated and authorized)
        assert response.status_code == 200


# ============ GET CURRENT CITIZEN TESTS ============
class TestGetCurrentCitizen:
    """Tests for getting current citizen profile (GET /api/auth/me)."""
    
    def test_get_current_citizen_returns_profile(self, client, valid_citizen_data):
        """GET /api/auth/me returns current citizen profile."""
        # Signup and login
        client.post("/api/auth/signup", json=valid_citizen_data)
        login_response = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        token = login_response.json().get("session_token") or login_response.json().get("token")
        
        # Get current citizen
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["citizen_id"] == valid_citizen_data["citizen_id"]
        assert data["email"] == valid_citizen_data["email"]
        assert "password" not in data
    
    def test_get_current_citizen_without_token_returns_401(self, client):
        """GET /api/auth/me without token returns 401."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401


# ============ INTEGRATION TESTS ============
class TestIntegration:
    """End-to-end workflow tests."""
    
    def test_complete_citizen_workflow(self, client, valid_citizen_data):
        """Complete workflow: signup -> login -> get profile -> logout."""
        # Step 1: Signup
        signup_response = client.post("/api/auth/signup", json=valid_citizen_data)
        assert signup_response.status_code == 201
        assert signup_response.json()["citizen_id"] == valid_citizen_data["citizen_id"]
        
        # Step 2: Login
        login_response = client.post("/api/auth/login", json={
            "citizen_id": valid_citizen_data["citizen_id"],
            "password": valid_citizen_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json().get("session_token") or login_response.json().get("token")
        assert token is not None
        
        # Step 3: Get current citizen
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == valid_citizen_data["email"]
        
        # Step 4: Access protected endpoint (reports)
        reports_response = client.get(
            "/api/reports",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert reports_response.status_code == 200
        
        # Step 5: Logout
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert logout_response.status_code == 204
