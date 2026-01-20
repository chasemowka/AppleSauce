# AppleSauce Project - Complete Context & Status

**Last Updated:** January 20, 2026  
**Repository:** https://github.com/chasemowka/AppleSauce

---

## Project Overview

A resume analysis and job matching application that:
1. Parses uploaded resumes (PDF/DOCX)
2. Fetches job postings from multiple sources
3. Matches resumes to relevant jobs with AI scoring
4. Provides resume optimization suggestions per job
5. Native iOS app with backend API

---

## Tech Stack

### iOS App (Mac Only)
- **Language:** Swift + SwiftUI
- **Platform:** iOS 14+
- **Features:** Resume upload, job browsing, suggestions sidebar
- **Location:** `ios-app/AppleSauce/AppleSauce/`

### Backend API (Cross-Platform)
- **Framework:** Python + FastAPI
- **Server:** Uvicorn
- **APIs:** AWS Jobs, Netflix (Greenhouse), RapidAPI/JSearch
- **Location:** `backend/`

### Web Preview (Testing Only)
- **Tech:** HTML/CSS/JavaScript
- **Purpose:** Visual preview of iOS UI in browser
- **Location:** `web-preview/`

---

## Project Structure

```
AppleSauce/
├── ios-app/
│   ├── AppleSauce/AppleSauce/
│   │   ├── AppleSauceApp.swift          # Main app entry
│   │   ├── ContentView.swift            # Tab navigation
│   │   ├── Models.swift                 # Data models
│   │   ├── APIService.swift             # Backend communication
│   │   ├── ResumeUploadView.swift       # Upload interface
│   │   ├── JobListingsView.swift        # Job list with API
│   │   └── JobDetailView.swift          # Job details + suggestions
│   ├── Components/
│   │   ├── JobCard.swift                # Reusable job card
│   │   ├── SuggestionCard.swift         # Suggestion UI
│   │   ├── UploadButton.swift           # Upload button
│   │   └── Sidebar.swift                # Navigation sidebar
│   ├── DesignSystem/
│   │   ├── Colors.swift                 # Color palette
│   │   └── Typography.swift             # Text styles
│   └── SETUP.md                         # iOS setup guide
│
├── backend/
│   ├── main.py                          # FastAPI app & routes
│   ├── requirements.txt                 # Python dependencies
│   ├── services/
│   │   ├── resume_parser.py             # PDF/DOCX parsing
│   │   ├── job_matcher.py               # Matching algorithm
│   │   └── job_api_service.py           # Job API integrations
│   └── JOB_API_SETUP.md                 # API setup guide
│
├── web-preview/
│   ├── index.html                       # iOS UI preview
│   └── server.py                        # Simple HTTP server
│
└── README.md                            # Project documentation
```

---

## Current Features

### ✅ Working Features

**Backend API:**
- Resume upload and parsing (PDF/DOCX)
- Job fetching from AWS careers (real API)
- Job matching with keyword scoring
- Resume suggestions endpoint
- CORS enabled for iOS app
- Interactive API docs at `/docs`

**iOS App:**
- Tab-based navigation
- Resume upload with document picker
- Job listings with API integration
- Job detail view with suggestions sidebar
- Network service for backend communication
- Design system with colors and components

**Web Preview:**
- Visual mockup of iOS app
- Three views: Upload, Jobs, Job Detail
- Works in any browser

### 🔄 In Progress

**Job API Integrations:**
- ✅ AWS/Amazon Jobs - Working perfectly
- ❌ Netflix Jobs - API blocked or changed
- ⚠️ Microsoft Jobs - Placeholder data only
- 🔜 Indeed/LinkedIn - Needs RapidAPI key
- 🔜 Oracle, L3Harris, OpenAI - Not yet implemented

---

## Setup Instructions

### Windows (Backend Development)

```bash
# Clone repo
git clone https://github.com/chasemowka/AppleSauce.git
cd AppleSauce

# Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run server
python main.py
```

**Test:** http://127.0.0.1:8000/docs

### Mac (iOS Development)

1. Open Xcode
2. Create new iOS App project named "AppleSauce"
3. Add all Swift files from `ios-app/AppleSauce/AppleSauce/`
4. Add network permissions to Info.plist:
   ```xml
   <key>NSAppTransportSecurity</key>
   <dict>
       <key>NSAllowsLocalNetworking</key>
       <true/>
   </dict>
   ```
5. Run in simulator (iPhone 14+)

**Full guide:** `ios-app/SETUP.md`

---

## API Endpoints

### Current Endpoints

**POST /upload-resume**
- Upload PDF or DOCX resume
- Returns parsed text

**GET /jobs**
- Query params: `query` (keywords), `source` (indeed/aws/netflix/all)
- Returns job listings from specified sources

**GET /jobs/company/{company}**
- Path param: company name (aws, netflix, microsoft, etc.)
- Query param: `keywords` (optional)
- Returns jobs from specific company

**POST /match**
- Body: `{"resume_text": "...", "query": "..."}`
- Returns scored job matches

**POST /suggestions**
- Body: `{"resume_text": "...", "job_id": 1}`
- Returns resume improvement suggestions

**GET /**
- Health check

---

## Dependencies

### Backend (Python)
```
fastapi==0.103.2
uvicorn==0.22.0
pypdf2==3.0.1
python-docx==0.8.11
python-multipart==0.0.5
requests==2.31.0
```

### iOS (Swift)
- No external dependencies
- Uses native SwiftUI and Foundation

---

## Environment Variables

### Optional: RapidAPI (Indeed/LinkedIn Data)

```bash
# Get free key: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# Free tier: 2,500 requests/month

# Windows
set RAPIDAPI_KEY=your_key_here

# Mac/Linux
export RAPIDAPI_KEY=your_key_here
```

---

## Testing

### Backend Testing
1. Start server: `python main.py`
2. Open: http://127.0.0.1:8000/docs
3. Test endpoints:
   - GET `/jobs/company/aws?keywords=python` ✅ Works
   - GET `/jobs/company/netflix?keywords=engineer` ❌ Returns empty
   - GET `/jobs?query=software engineer&source=all`

### iOS Testing
1. Run in Xcode simulator
2. Navigate to "Job Listings" tab
3. Should load jobs from backend
4. Click job to see details and suggestions

### Web Preview Testing
```bash
cd web-preview
python -m http.server 8080
```
Open: http://localhost:8080

---

## Known Issues

1. **Netflix API** - Returns 0 jobs (API might be blocking or changed)
2. **Microsoft API** - Returns placeholder data (needs authentication)
3. **Node.js on Linux** - GLIBC version issue (use Python server instead)
4. **Windows localhost** - Use `127.0.0.1` instead of `localhost`

---

## Next Steps / TODO

### High Priority
- [ ] Add RapidAPI key for Indeed/LinkedIn integration
- [ ] Fix Netflix job fetching
- [ ] Implement Microsoft authentication
- [ ] Add job caching to reduce API calls
- [ ] Store uploaded resumes in database

### Medium Priority
- [ ] Integrate AWS Bedrock for AI suggestions
- [ ] Add user authentication
- [ ] Implement resume storage (S3)
- [ ] Add more company integrations (Oracle, L3Harris, OpenAI)
- [ ] Create database schema (SQLite/PostgreSQL)

### Low Priority
- [ ] Add unit tests
- [ ] Implement rate limiting
- [ ] Add job bookmarking
- [ ] Email notifications for new matches
- [ ] Export resume suggestions as PDF

---

## Development Workflow

### Making Changes

**On Windows (Backend):**
1. Make changes to Python files
2. Server auto-reloads (if started with `--reload`)
3. Test in `/docs` page
4. Commit: `git add . && git commit -m "message" && git push`

**On Mac (iOS):**
1. Pull latest: `git pull`
2. Make changes in Xcode
3. Test in simulator
4. Commit and push

### Git Workflow
```bash
# Pull latest
git pull

# Make changes
# ...

# Commit
git add .
git commit -m "Descriptive message"
git push
```

---

## Architecture Decisions

### Why Swift/SwiftUI?
- Native iOS performance
- Best user experience
- Access to all iOS features
- Future App Store deployment

### Why FastAPI?
- Fast and modern Python framework
- Automatic API documentation
- Easy AI/ML integration
- Great for AWS services

### Why Separate Backend?
- iOS app can be lightweight
- Backend can scale independently
- Easy to add web/Android later
- Can deploy backend to AWS Lambda

---

## Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- SwiftUI: https://developer.apple.com/xcode/swiftui/
- AWS Jobs API: https://www.amazon.jobs/en/search.json
- RapidAPI JSearch: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

### Project Files
- Main README: `README.md`
- iOS Setup: `ios-app/SETUP.md`
- Job API Setup: `backend/JOB_API_SETUP.md`
- This Document: `PROJECT_CONTEXT.md`

---

## Team / Contributors

- **Developer:** Chase Mowka
- **Repository:** Private (https://github.com/chasemowka/AppleSauce)
- **Purpose:** Personal project / Potential iOS app

---

## Session Notes

### Session 1 (Jan 20, 2026)
- Created initial project structure
- Built iOS app with SwiftUI
- Created Python FastAPI backend
- Added web preview for testing
- Integrated AWS jobs API ✅
- Attempted Netflix integration ❌
- Added placeholder for Microsoft
- Tested on Windows successfully
- All code committed to GitHub

### Current Status
- Backend running on Windows
- iOS app ready for Mac testing
- AWS jobs working perfectly
- Need to add RapidAPI key for more sources
- Ready to continue development

---

## Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
python main.py

# Web Preview
cd web-preview
python -m http.server 8080

# Git
git pull
git add .
git commit -m "message"
git push

# Test API
curl http://127.0.0.1:8000/jobs/company/aws?keywords=python
```

---

**End of Context Document**

*This document contains everything needed to resume development at any time.*
