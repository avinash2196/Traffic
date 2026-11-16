# RoadWatch MVP - Quick Reference Card 🎯

## Start Everything (Choose One)

### Windows
```powershell
START-ALL.bat
# or
powershell -ExecutionPolicy Bypass -File START-ALL.ps1
```

### macOS/Linux
```bash
chmod +x START-ALL.sh
./START-ALL.sh
```

---

## Access Services

| Portal | URL | Purpose |
|--------|-----|---------|
| **Citizen** | http://127.0.0.1:3001/ | Submit reports, track status |
| **Officer** | http://127.0.0.1:3002/ | Review queue, approve/reject |

---

## Service Ports

| Service | Port | Status |
|---------|------|--------|
| Auth | 9001 | User management |
| Citizen API | 9002 | Reports & media |
| Officer API | 9003 | Review queue |
| Citizen Portal | 3001 | Frontend |
| Officer Portal | 3002 | Frontend |

---

## 15-Minute Test Flow

### Citizen (5 min)
1. Go to: http://127.0.0.1:3001/
2. Sign up (any username/email)
3. Click "Create Report"
4. Upload a photo
5. Submit report
6. View in "My Reports"

### Officer (5 min)
1. Go to: http://127.0.0.1:3002/
2. Sign up as officer
3. Go to "Review Queue"
4. Click a report
5. Approve or Reject
6. Award points

### Citizen (5 min)
1. Go back to http://127.0.0.1:3001/
2. Check "My Reports"
3. See officer's decision
4. ✅ Done!

---

## Documentation Files

| File | Read When | Time |
|------|-----------|------|
| `START-HERE.md` | First (navigation) | 2 min |
| `READY-TO-TEST.md` | Want to test now | 5 min |
| `SYSTEM-STATUS.md` | Need full details | 15 min |
| `QUICK-START.md` | Need quick ref | 2 min |
| `README.md` | Want project info | 10 min |

---

## Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| Services won't start | See SYSTEM-STATUS.md → Troubleshooting |
| Media won't load | Delete `roadwatch.db`, restart |
| Port already in use | Kill process on port, restart |
| Login broken | Clear browser cache, check logs |
| Database error | Delete `roadwatch.db`, restart |

---

## Developer Paths

### I want to test
```
1. Run: START-ALL.bat
2. Wait: 20 seconds
3. Open: http://127.0.0.1:3001/
4. Read: READY-TO-TEST.md
```

### I want to understand
```
1. Read: START-HERE.md
2. Read: SYSTEM-STATUS.md
3. Check: README.md
```

### I want to debug
```
1. Open: Developer Tools (F12)
2. Check: Console for errors
3. Check: Network tab for API calls
4. Check: Service logs in terminal
5. See: SYSTEM-STATUS.md → Troubleshooting
```

### I want to modify code
```
1. Edit file
2. Stop service (close window)
3. Run: START-ALL.bat
4. Test changes
```

---

## Common Commands

```bash
# View git log (recent changes)
git log --oneline -10

# Check which services are running
netstat -ano | findstr :3001  # Windows
lsof -i :3001                 # macOS/Linux

# Delete database to reset
rm roadwatch.db              # macOS/Linux
del roadwatch.db             # Windows

# Run single service
cd citizen
python -m uvicorn app:app --port 9002
```

---

## File Locations

| Item | Location |
|------|----------|
| **Database** | `./roadwatch.db` |
| **Media** | `./citizen/media_store/` |
| **Auth Service** | `./auth/` |
| **Citizen API** | `./citizen/` |
| **Officer API** | `./officer/` |
| **Citizen Portal** | `./citizen-app/` |
| **Officer Portal** | `./officer-app/` |

---

## Key Features Ready

✅ Citizen sign up & login  
✅ Create violation report  
✅ Upload photo/video  
✅ Submit to queue  
✅ Officer review queue  
✅ Officer approval/rejection  
✅ Point assignment  
✅ Status tracking  
✅ Media persistence  
✅ Database persistence  

---

## API Endpoints (Reference)

```
POST   /api/auth/login
POST   /api/auth/register
POST   /api/reports
GET    /api/reports
GET    /api/reports/{id}
POST   /api/media/upload
GET    /api/media/{file_path}
```

---

## Browser DevTools Tips

```javascript
// Check auth token
console.log(localStorage.getItem('citizen_token'))

// Check last API response
// Open DevTools → Network tab → click request → Response tab

// Clear auth and logout
localStorage.clear()
```

---

## System Requirements

- Python 3.8+
- Browser (Chrome/Firefox/Safari/Edge)
- Port availability: 3001, 3002, 9001, 9002, 9003
- ~100MB disk space
- SQLite (included with Python)

---

## What's NOT Included (Phase 2)

- Real authentication (uses demo tokens)
- AI image screening (Gemini/OpenAI integration)
- PostgreSQL (uses SQLite for MVP)
- Real-time notifications
- Mobile app
- Maps integration
- PDF exports
- Email notifications

---

## Next Steps After Testing

1. **Document findings** - What worked? What broke?
2. **Report issues** - Create GitHub issues for bugs
3. **Plan Phase 2** - AI integration, PostgreSQL, etc.
4. **Code review** - Review architecture for Phase 2
5. **Performance testing** - Load test with multiple users

---

## Get Help

1. **Quick question** → See QUICK-START.md
2. **Need details** → See SYSTEM-STATUS.md
3. **Lost?** → See START-HERE.md
4. **Want overview** → See README.md
5. **Can't start** → Delete roadwatch.db, restart

---

## Status ✅

- **MVP**: Ready for testing
- **Services**: All running
- **Documentation**: Complete
- **One-Click Startup**: Implemented
- **Test Scenarios**: Ready

**Ready to test? Run: `START-ALL.bat` or `./START-ALL.sh`**

---

Last Updated: 2026-11-15  
Version: MVP 1.0
