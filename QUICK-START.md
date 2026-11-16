# RoadWatch Traffic MVP - Quick Start Guide

## 🚀 One-Click Startup

### Windows Users
Double-click one of these files:
- **`START-ALL.bat`** - Easiest, launches PowerShell script
- **`START-ALL.ps1`** - PowerShell version

Or from PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File START-ALL.ps1
```

### macOS / Linux Users
From terminal:
```bash
chmod +x START-ALL.sh
./START-ALL.sh
```

---

## 📍 What Gets Started

When you run the startup script, it automatically launches:

| Service | Port | Purpose |
|---------|------|---------|
| **Auth Service** | 9001 | User authentication & registration |
| **Citizen API** | 9002 | Citizen-facing API (report submission, media) |
| **Officer API** | 9003 | Officer-facing API (review queue, decisions) |
| **Citizen Portal** | 3001 | Citizen web interface |
| **Officer Portal** | 3002 | Officer web interface |

---

## 🧪 Testing the System

### Citizen Flow (Submit a Report)
1. Open browser: **http://127.0.0.1:3001/**
2. Click "Sign Up"
3. Create account (any email/password)
4. Click "Report"
5. Fill in:
   - Violation Type: Select one
   - Vehicle Number: e.g., "DL-01-AB-1234"
   - Location: e.g., "Main Street"
   - Upload photo/video
6. Click "Submit"
7. View your report in "My Reports"

### Officer Flow (Review Reports)
1. Open browser: **http://127.0.0.1:3002/**
2. Click "Sign Up" (as officer)
3. Create account (any email/password)
4. Click "Review Queue"
5. See all submitted reports
6. Click report to view details
7. Click "Review" to make decision:
   - Approve (awards provisional points)
   - Reject (dismiss report)

---

## 🛑 Stopping Services

The startup window stays open to show you the status. To stop everything:
- **Windows**: Close the PowerShell window
- **macOS/Linux**: Press `Ctrl+C` in the terminal

Or manually close individual service windows to stop specific services.

---

## 🐛 Troubleshooting

### Services Won't Start
- Check if ports 9001-9003, 3001-3002 are already in use
- On Windows, try: `netstat -ano | findstr :9001`
- Kill any existing processes using those ports

### Media Won't Load in Reports
- Make sure Citizen API (9002) is running
- Check browser console for errors (F12)
- Media files should be in `./citizen/media_store/`

### Login Fails
- Make sure Auth Service (9001) is running
- Clear browser cookies and try again
- Check auth service logs

### Database Issues
- SQLite database is stored in `./roadwatch.db`
- Delete it to start fresh: `rm roadwatch.db`
- Services will recreate it on next startup

---

## 📊 Viewing Logs

Each service logs to its own PowerShell window. You can see:
- API startup messages
- Request logs (incoming HTTP requests)
- Database operations
- Error messages

On macOS/Linux, logs are saved to:
- `logs-auth.txt`
- `logs-citizen-api.txt`
- `logs-officer-api.txt`
- `logs-citizen-app.txt`
- `logs-officer-app.txt`

---

## 🔑 Demo Mode Features

This MVP uses demo authentication:
- **Citizen ID**: Passed via `X-Citizen-Id` header (auto-handled by frontend)
- **Officer Token**: Shared token mode (all officers see all reports)
- **No Real Auth**: Uses JWT internally but easy to override for testing

To test as different users:
- Open in different browser profiles, or
- Use incognito/private mode for each user

---

## 📚 Architecture

```
┌─────────────────────────────────────────────────┐
│         Browser (User Interface)                │
├──────────────────┬──────────────────────────────┤
│  Citizen Portal  │  Officer Portal              │
│    (3001)        │   (3002)                     │
└────────┬─────────┴──────────┬────────────────────┘
         │                    │
    ┌────▼─────┐        ┌─────▼────┐
    │ Citizen   │        │ Officer  │
    │ API       │        │ API      │
    │ (9002)    │        │ (9003)   │
    └────┬──────┘        └──────┬───┘
         │                      │
         └──────────┬───────────┘
                    │
              ┌─────▼─────┐
              │Auth Service│
              │   (9001)   │
              └────┬───────┘
                   │
            ┌──────▼──────┐
            │ Shared SQLite│
            │  Database   │
            │roadwatch.db │
            └─────────────┘
```

---

## 🎯 Next Steps

After everything is running:

1. **Test citizen flow** - Submit a report with photo/video
2. **Test officer flow** - Review the submitted report
3. **Check media loading** - Verify images/videos display correctly
4. **Test decisions** - Approve/reject reports and see status updates
5. **Review logs** - Check service logs for any errors

---

## ❓ Questions?

- Check the logs in each service window
- Review the architecture in `ARCHITECTURE-DECISION-FRAMEWORK.md`
- Look at test files in `tests/` for API examples
- Check `README.md` for project overview

---

**Enjoy testing RoadWatch! 🚗🚔**
