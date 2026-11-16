# Contributing to RoadWatch Traffic

Thank you for your interest in contributing to RoadWatch! This guide explains our development workflow, code standards, and how to submit changes.

---

## 🏗️ Development Workflow (Prompt-Driven Development)

We follow **Prompt-Driven Development (PDD)** for all code changes:

1. **Plan**: Create a detailed Implementation Plan
2. **Approve**: Get human review & approval
3. **Implement**: Write code following the plan
4. **Review**: Code review against the plan
5. **Verify**: Tests pass, no regressions
6. **Commit**: Merge to main branch

**No code changes without an approved Implementation Plan.**

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/avinash2196/Traffic.git
cd Traffic
```

### 2. Set Up Development Environment
```bash
# Copy configuration template
copy .env.example .env

# Edit .env with your API keys
# OPENAI_API_KEY=sk-...
# GEMINI_API_KEY=...
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 5. Run Tests
```bash
.\run-tests.ps1
```

---

## 📋 Folder Structure

```
Traffic/
├── auth/                      # Authentication microservice
├── citizen/                   # Citizen API
├── officer/                   # Officer API
├── ai-gateway/                # AI screening service
├── ai-worker/                 # Background AI processor
├── citizen-app/               # Citizen frontend
├── officer-app/               # Officer frontend
├── shared/                    # Shared utilities & database
├── tests/                     # Test suite (pytest)
├── tools/                     # Development utilities
├── docs/                      # Documentation
│   └── .archived/             # Archived documentation
├── README.md                  # Main project overview
├── QUICK-START.md             # 5-minute setup guide
└── CONTRIBUTING.md            # This file
```

---

## 🔄 Git Workflow

### Creating a Feature Branch
```bash
git checkout -b feature/your-feature
# or for fixes:
git checkout -b fix/bug-description
# or for cleanup:
git checkout -b cleanup/cleanup-description
```

### Making Changes
1. Edit files in your feature branch
2. Test your changes: `.\run-tests.ps1`
3. Verify no broken imports or dependencies
4. Stage changes: `git add .`
5. Commit: `git commit -m "Brief description..."`

### Push and Create PR
```bash
git push origin feature/your-feature
# Then create a Pull Request on GitHub
```

### Commit Message Format
```
Brief one-line summary (50 chars max)

Longer explanation of what changed and why.
Can be multiple paragraphs.

Fixes #123 (if fixing an issue)
Relates to #456 (if related to other work)

Co-authored-by: Your Name <your.email@example.com>
```

---

## ✅ Code Standards

### Python Style
- Use type hints at public boundaries
- PEP 8 compliant
- Docstrings for public functions
- No `except: pass` - always handle explicitly

### Async Code
- Use `async`/`await` for I/O-bound operations
- FastAPI endpoints should be async
- Use `pytest-asyncio` for async tests

### Database Interactions
- Use parameterized queries (never build SQL from user input)
- Explicit transaction boundaries
- Handle connection errors gracefully
- Document any schema changes

### Testing
- Write tests first (RED phase)
- Tests should be independent
- Use descriptive test names
- Mock external services (OpenAI, etc.)
- Aim for >80% code coverage

---

## 🧪 Testing

### Run All Tests
```bash
.\run-tests.ps1
```

### Run Specific Test File
```bash
pytest tests/test_citizen_api.py -v
```

### Run Specific Test
```bash
pytest tests/test_citizen_api.py::test_submit_report -v
```

### With Coverage
```bash
pytest tests/ --cov=shared --cov-report=html
```

---

## 🚀 Starting Services

### Start Everything
```bash
.\START-ALL.ps1
```

### Start Microservices Only
```bash
.\start-services.ps1
```

### Start Frontends Only
```bash
.\start-frontends.ps1
```

### Available Endpoints
- **Auth Service:** http://127.0.0.1:9003/
- **Citizen API:** http://127.0.0.1:9001/
- **Officer API:** http://127.0.0.1:9002/
- **AI Gateway:** http://127.0.0.1:9004/
- **Citizen App:** http://127.0.0.1:3001/
- **Officer App:** http://127.0.0.1:3002/

---

## 🔐 Security Guidelines

### Secrets Management
- **Never commit** `.env` file (it's in .gitignore)
- **Never hardcode** API keys or tokens
- **Use environment variables** for all secrets
- **Document template** in `.env.example`

### Code Review Checklist
- [ ] No secrets in code or logs
- [ ] Parameterized queries (no SQL injection)
- [ ] Input validation before database operations
- [ ] Proper HTTP status codes (401 auth, 403 permission, 400 validation)
- [ ] Error messages don't leak sensitive info

---

## 📚 Architecture & Design

### Microservices Design
- Each service is independent (can run separately)
- Services communicate via HTTP REST API
- Database is shared (SQLite for MVP, PostgreSQL for production)
- No circular dependencies between services

### API Contract
- Endpoints documented in service app.py
- Use Pydantic for request/response validation
- Swagger UI available at `/docs` on each service
- Versioning via URL path (e.g., `/api/v1/reports`)

### Authentication
- **MVP:** Demo token via X-Citizen-Id header
- **Production:** OIDC token validation
- Auth service validates all tokens
- Each endpoint checks authorization

---

## 🐛 Reporting Bugs

If you find a bug:
1. **Search existing issues** to avoid duplicates
2. **Create detailed issue** with:
   - Expected behavior
   - Actual behavior
   - Steps to reproduce
   - Environment (Python version, OS, etc.)
3. **Assign labels** (bug, urgent, etc.)

---

## 💡 Proposing Features

For new features:
1. **Open a discussion** before coding
2. **Describe the feature** and use case
3. **Discuss trade-offs** with maintainers
4. **Get approval** before implementation
5. **Follow PDD workflow** for the feature

---

## 📖 Documentation

### Where to Find Docs
- **README.md** - Project overview
- **QUICK-START.md** - 5-minute setup
- **docs/ARCHITECTURE.md** - Architecture decisions
- **docs/TESTING.md** - Testing guide
- **docs/DEPLOYMENT.md** - Deployment instructions
- **docs/.archived/** - Historical planning docs

### Writing Documentation
- Use Markdown format
- Keep it concise and clear
- Include code examples
- Link to related docs
- Update when code changes

---

## 🤝 Code Review Process

### Before Requesting Review
- [ ] Run all tests: `.\run-tests.ps1`
- [ ] Update documentation
- [ ] Commit message is clear
- [ ] No debugging code left in
- [ ] No secrets or sensitive data

### Review Standards
- Reviewers check **correctness** and **plan adherence**
- Must pass CI/CD checks
- At least 1 approval required
- Maintainer resolves merge conflicts

### Common Review Comments
- "Does this follow the Implementation Plan?" → Adjust to plan
- "Add test for this edge case" → Add test
- "Update API documentation" → Update docs
- "Consider security implications" → Review security

---

## 🚦 CI/CD Pipeline

Automated checks on every PR:
- ✅ Linting (Python style)
- ✅ Type checking
- ✅ Unit tests
- ✅ Integration tests
- ✅ Secret scanning

All checks must pass before merge.

---

## 📞 Getting Help

- **GitHub Issues:** Ask questions or report bugs
- **GitHub Discussions:** Propose ideas
- **Code Comments:** Ask clarifications in PR reviews
- **Documentation:** Check docs/ folder first

---

## 🎓 Project Structure Resources

- **Plan.md** - Master project breakdown
- **docs/ARCHITECTURE.md** - Design decisions
- **docs/.ai/** - AI planning documents
- **docs/.archived/** - Historical documentation

---

**Thank you for contributing to RoadWatch! 🚗**
