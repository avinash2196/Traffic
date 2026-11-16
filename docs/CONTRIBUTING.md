# Contributing to RoadWatch

Thank you for your interest in contributing to RoadWatch! This document explains how to set up your development environment, follow our development process, and submit changes.

---

## 📋 Quick Start for Contributors

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Traffic.git
cd Traffic
```

### 2. Set Up Local Environment
```bash
# macOS/Linux
chmod +x start.sh
./start.sh

# Windows
.\start-windows.ps1

# OR Manual setup
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR .venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 3. Verify Setup
```bash
# Run tests
pytest tests/

# Start the app
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### 4. Access the Application
- Citizen portal: http://127.0.0.1:8000/citizen-login.html
- Officer portal: http://127.0.0.1:8000/officer-login.html
- API docs: http://127.0.0.1:8000/api/docs

---

## 🏗️ Project Structure

```
Traffic/
├── app.py                     # FastAPI application (main entry point)
├── bootstrap.py               # Database schema & initialization
├── media.py                   # Media file validation & processing
├── requirements.txt           # Python dependencies
├── tests/
│   └── test_api.py           # Integration tests (10 tests)
├── templates/                 # HTML pages (8 templates)
│   ├── citizen-*.html
│   └── officer-*.html
├── static/
│   ├── css/                   # Stylesheets (4 files)
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── responsive.css
│   └── js/                    # JavaScript utilities (4 files)
│       ├── api.js
│       ├── auth.js
│       ├── common.js
│       └── utils.js
├── media_store/               # User-uploaded media (local storage)
├── Dockerfile                 # Docker build configuration
├── start.sh / start-windows.ps1  # Startup scripts
├── .env.example              # Environment variable template
├── Plan.md                    # Architecture & design decisions
├── COMPLETION.md             # Project status summary
├── LOCAL_DEPLOYMENT.md       # Local setup guide
├── GCP_DEPLOYMENT.md         # Production deployment guide
├── QUICK_REFERENCE.md        # Quick lookup cheat sheet
├── INDEX.md                  # Documentation index
└── CONTRIBUTING.md           # This file

Key Files:
- app.py: 650+ lines, all 7 API endpoints + 8 HTML routes
- bootstrap.py: Database schema with 3 tables
- tests/test_api.py: 10 integration tests, 100% pass rate
```

---

## 🔄 Development Workflow (Prompt-Driven Development)

RoadWatch uses **Prompt-Driven Development (PDD)** with strict control boundaries:

### 1. **Before Writing Code**
- Review **Plan.md** to understand the project scope
- Check if your feature is listed in the milestones
- Open a GitHub Issue to discuss your idea (get approval first)

### 2. **Create a Feature Branch**
```bash
git checkout -b feature/my-feature
# OR for bug fixes:
git checkout -b bugfix/my-bug
# OR for documentation:
git checkout -b docs/my-docs
```

### 3. **Make Your Changes**
- Follow the code style guidelines (see below)
- Write tests for new functionality (RED phase)
- Implement the feature (GREEN phase)
- All tests must pass before committing

### 4. **Test Your Changes**
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Test specific file
pytest tests/test_api.py::test_citizen_submit_report
```

### 5. **Commit Your Changes**
```bash
git add .
git commit -m "[MILESTONE] Brief description

Longer explanation of what changed and why.

As per Plan.md Milestone M5, approved by <reviewer>.
Implementation Plan: <link or date>.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

### 6. **Push and Create Pull Request**
```bash
git push origin feature/my-feature
```

Then create a PR on GitHub with:
- Reference to the GitHub Issue
- Summary of changes
- Tests added/modified
- Any breaking changes noted

### 7. **Code Review**
- Address feedback from reviewers
- Ensure CI/CD checks pass
- Wait for approval before merging

### 8. **Merge and Deploy**
- After approval, squash/merge to main
- Monitor for any issues in production
- Update STATUS.md with completion

---

## 📐 Code Style & Conventions

### Python (app.py, bootstrap.py, media.py, tests/)

**Type Hints:**
```python
# Good: Explicit types at public boundaries
def create_report(data: ReportCreateRequest) -> ReportResponse:
    ...

# Bad: Missing types
def create_report(data):
    ...
```

**Function Documentation:**
```python
def validate_media(file: UploadFile) -> dict:
    """Validate uploaded media file.
    
    Args:
        file: Uploaded media file object
        
    Returns:
        Dictionary with validation result and metadata
        
    Raises:
        ValueError: If file is invalid or too large
    """
    ...
```

**Error Handling:**
```python
# Good: Explicit error handling
try:
    data = validate_media(file)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

# Bad: Silent failures
try:
    data = validate_media(file)
except:
    pass
```

**Database Interactions:**
```python
# Good: Use parameterized queries
cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))

# Bad: String concatenation (SQL injection risk!)
cursor.execute(f"SELECT * FROM reports WHERE id = {report_id}")
```

### HTML & CSS (templates/, static/)

**HTML:**
```html
<!-- Good: Semantic HTML, proper labels -->
<label for="violation-type">Violation Type:</label>
<select id="violation-type" name="type" required>
    <option value="">Select...</option>
    <option value="helmet">Riding without helmet</option>
</select>

<!-- Bad: Non-semantic, missing labels -->
<input type="text" name="type">
```

**CSS:**
```css
/* Good: Mobile-first, accessible */
.button {
    padding: 12px 16px;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
}

.button:focus {
    outline: 2px solid blue;
}

@media (max-width: 640px) {
    .button { padding: 10px 12px; }
}

/* Bad: Fixed sizes, no mobile support */
.button { width: 200px; height: 40px; }
```

**JavaScript:**
```javascript
// Good: Clear names, error handling
async function downloadEvidence(reportId) {
    try {
        const response = await fetch(`/api/authority/reports/${reportId}/evidence.zip`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const blob = await response.blob();
        downloadFile(blob, `evidence-${reportId}.zip`);
    } catch (error) {
        showToast(`Download failed: ${error.message}`, 'error');
    }
}

// Bad: Unclear names, no error handling
function download(id) {
    fetch(`/api/reports/${id}`);
}
```

### Database Schema

```python
# Good: Clear constraints, descriptive names
CREATE TABLE reports (
    id TEXT PRIMARY KEY,
    citizen_id TEXT NOT NULL,
    violation_type TEXT NOT NULL,
    status TEXT NOT NULL,  -- Submitted, Evidence screening, etc.
    points INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (citizen_id) REFERENCES citizens(id)
);

# Bad: Vague names, missing constraints
CREATE TABLE r (
    id TEXT,
    cid TEXT,
    type TEXT,
    st TEXT
);
```

---

## 🧪 Testing Guidelines

### Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    """Fixture for test API client."""
    return TestClient(app)

def test_citizen_submit_report(client):
    """Test that citizen can submit a new report."""
    # Arrange: Set up test data
    report_data = {
        "violation_type": "helmet",
        "location": "New Delhi",
        "media_files": ["test.jpg"]
    }
    
    # Act: Call the API
    response = client.post(
        "/api/reports",
        json=report_data,
        headers={"X-Citizen-Id": "test_user_123"}
    )
    
    # Assert: Verify the response
    assert response.status_code == 201
    data = response.json()
    assert "report_id" in data
    assert data["status"] == "Submitted"
```

### Test Naming

```python
# Good: Descriptive, says what's being tested
def test_citizen_submit_report_with_valid_data():
def test_officer_cannot_access_citizen_reports():
def test_invalid_media_returns_400():

# Bad: Vague, unclear
def test_api():
def test_submit():
def test_error():
```

### Test Coverage

- **Unit tests:** Individual functions (validate_media, format_timestamp, etc.)
- **Integration tests:** Full API workflows (citizen submit → officer review)
- **Error cases:** Invalid input, missing fields, authorization failures
- **Edge cases:** Empty strings, large files, concurrent requests

Run coverage report:
```bash
pytest --cov=. --cov-report=html tests/
# Opens htmlcov/index.html in browser
```

---

## 🔐 Security Guidelines

### Never Commit Secrets

```python
# Bad: API key in code
OPENAI_API_KEY = "sk-abc123xyz789"
REVIEWER_TOKEN = "hardcoded-token"

# Good: Load from environment
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REVIEWER_TOKEN = os.getenv("ROADWATCH_REVIEWER_TOKEN")
```

### Input Validation

```python
# Good: Validate all user input
def create_report(data: ReportCreateRequest):
    if not data.violation_type or data.violation_type not in VALID_TYPES:
        raise ValueError("Invalid violation type")
    if len(data.location) > 500:
        raise ValueError("Location too long")
    # Process...

# Bad: Trust user input
def create_report(data):
    store_report(data)  # No validation!
```

### Access Control

```python
# Good: Check authorization before returning data
@app.get("/api/reports/{report_id}")
def get_report(report_id: str, x_citizen_id: str = Header()):
    report = get_report_from_db(report_id)
    if report.citizen_id != x_citizen_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return report

# Bad: No authorization check
@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    return get_report_from_db(report_id)  # Anyone can view!
```

---

## 📚 Documentation Guidelines

### Code Comments

```python
# Good: Explain WHY, not WHAT
# SQLite WAL mode improves concurrency for multi-threaded access
PRAGMA journal_mode = WAL;

# Use SHA-256 because it's fast and good for duplicate detection
# (not for cryptographic security)
file_hash = hashlib.sha256(file_contents).hexdigest()

# Bad: Obvious comments
# Initialize the database
init_database()

# Convert string to int
value = int(value)
```

### README & Documentation

- Keep README.md for users (overview, quick start)
- Use LOCAL_DEPLOYMENT.md for developers (setup details)
- Use GCP_DEPLOYMENT.md for production (deployment steps)
- Use QUICK_REFERENCE.md for quick lookup
- Update relevant docs when adding features

### API Documentation

```python
# Good: Clear request/response models with docstrings
class ReportCreateRequest(BaseModel):
    """Request to create a new violation report."""
    violation_type: str  # One of: helmet, triple_riding, red_light
    location: str        # Physical location description (max 500 chars)
    media_files: List[str] = []  # File paths or URLs (optional)

# Uses Swagger UI auto-generation:
# POST /api/reports → See request/response schema
```

---

## 🚀 Performance & Scalability

### Database Queries

```python
# Good: Use indexes for frequently queried columns
# (Already done: See bootstrap.py)
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_media_report_id ON media(report_id);

# Good: Limit result sets
def get_reports(page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    return db.query(Report).offset(offset).limit(page_size)

# Bad: Fetch all rows at once
def get_reports():
    return db.query(Report).all()  # Could be millions of rows!
```

### API Performance

```python
# Good: Cache responses where appropriate
@app.get("/api/authority/queue", cache=300)  # Cache for 5 minutes
def get_queue():
    ...

# Good: Use pagination for large result sets
@app.get("/api/reports")
def list_reports(page: int = Query(1), page_size: int = Query(20, le=100)):
    # le=100 enforces maximum page size
    ...
```

---

## 🐛 Bug Reporting

Found a bug? Open a GitHub Issue with:

1. **Title:** Clear, concise description
   - Good: "Citizen can't upload MP4 files"
   - Bad: "File upload broken"

2. **Description:**
   - What you were trying to do
   - What happened instead
   - What you expected to happen

3. **Reproduction Steps:**
   ```
   1. Login as citizen
   2. Click "Report Violation"
   3. Try to upload file.mp4
   4. See error: "File type not supported"
   ```

4. **Environment:**
   - OS: Windows 10 / macOS 12 / Ubuntu 20.04
   - Python version: 3.11.5
   - Browser: Chrome 120

5. **Screenshots:** If UI-related, include screenshots

---

## 💡 Feature Requests

Want to suggest a new feature? Open a GitHub Issue with:

1. **Title:** Feature request — [description]
   - Good: "Feature request — Add email notifications"
   - Bad: "New feature"

2. **Description:** Explain the feature and why it's needed

3. **Acceptance Criteria:** How will we know it's done?
   ```
   - [ ] Officer can enable email notifications in settings
   - [ ] Officers receive email when report assigned
   - [ ] Emails include report summary + evidence link
   - [ ] Officers can unsubscribe
   ```

4. **Related Issues:** Link to any existing discussions

---

## 📝 Commit Message Format

```
[MILESTONE] Brief description (50 chars max)

Longer explanation of the change. Explain:
- What problem does this solve?
- Why this approach?
- Any tradeoffs or alternatives considered?

If fixes an issue:
Fixes #123

As per Plan.md Milestone M5 (UI Implementation), approved by @reviewer.
Implementation Plan: https://github.com/...

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

### Milestone Abbreviations

```
[M1] Database schema
[M2] FastAPI app
[M3.1] Media upload (tests)
[M3.2] Media upload (implementation)
[M4.1] API endpoints (tests)
[M4.2] API endpoints (implementation)
[M5] UI (citizen + officer)
[M6] Evidence export (ZIP)
[M7] Docker & deployment
[DOCS] Documentation
[CI/CD] Pipeline updates
[BUG] Bug fix
```

---

## 🔍 Code Review Checklist

When reviewing pull requests, check for:

### Correctness
- [ ] Code changes match the PR description
- [ ] Tests pass (10/10 tests for API, etc.)
- [ ] No breaking changes (or documented breaking changes)
- [ ] Error handling is explicit (no silent failures)
- [ ] Database queries use parameterized statements (no SQL injection)

### Security
- [ ] No secrets in code or logs
- [ ] Input validation on all user data
- [ ] Authorization checks before data access
- [ ] CORS/CSRF protection (if applicable)

### Performance
- [ ] No N+1 queries
- [ ] Appropriate pagination for large result sets
- [ ] Response times acceptable (< 500ms)

### Testing
- [ ] New features have tests
- [ ] Edge cases covered
- [ ] Test names descriptive
- [ ] All tests pass

### Documentation
- [ ] Code comments explain WHY
- [ ] Function docstrings present
- [ ] README/guide updated (if needed)
- [ ] API docs accurate (if endpoint changed)

---

## 🎯 Getting Help

- **Questions about code?** Check app.py comments or ask in GitHub Issues
- **Setup problems?** See LOCAL_DEPLOYMENT.md troubleshooting
- **Architecture questions?** Read Plan.md or ARCHITECTURE.md
- **Deployment help?** See GCP_DEPLOYMENT.md
- **Test failures?** Run `pytest -v tests/` to see detailed output

---

## 📋 Contributor License Agreement

By contributing to RoadWatch, you agree that:
- Your contributions can be used under the project's license
- You have the right to contribute the code
- Your contributions are original works

---

## 🙏 Thank You!

Your contributions make RoadWatch better. Here's what we're most grateful for:

1. **Bug reports** — Help us identify and fix issues
2. **Documentation** — Improve guides and examples
3. **Feature ideas** — Shape the product roadmap
4. **Code contributions** — Implement features and fixes
5. **Feedback** — Tell us what works and what doesn't

---

## 📞 Questions?

- GitHub Issues: For bugs, features, questions
- GitHub Discussions: For general chat
- Email: (If applicable, add contact email)

**Happy contributing!** 🎉

