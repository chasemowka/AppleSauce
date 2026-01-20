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

## Development Environment Notes

### Linux Environment (Current)
- ✅ Backend development fully supported
- ✅ API testing and integration
- ✅ Web preview for UI visualization
- ❌ Cannot run Xcode (Mac only)
- ❌ Cannot test iOS app directly
- ✅ Can use web preview at `web-preview/index.html`

### Mac Environment (Required for iOS)
- ✅ Full iOS app development
- ✅ Xcode for building and testing
- ✅ iOS Simulator
- ✅ Deploy to physical iPhone
- Installation: App Store → Search "Xcode" → Install (free, ~15GB)

### Testing Options on Linux
1. **Backend API Testing:** http://127.0.0.1:8000/docs
2. **Web Preview:** `cd web-preview && python -m http.server 8080`
3. **API Calls:** Use curl or Postman to test endpoints

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

### ✅ Working Features

**iOS App:**
- Dashboard home page with stats and quick actions
- Job search with circular match indicators (color-coded)
- Job listings view with real-time data
- Resume upload interface
- Tab navigation (Dashboard, Search, Jobs, Upload)
- Swift 6 compatible codebase
- Running in Xcode iOS Simulator

**Backend API:**
- Resume parsing (PDF/DOCX)
- Job fetching from multiple sources
- Security clearance filtering
- Job matching with keyword scoring
- Resume suggestions endpoint
- CORS enabled for iOS app
- Interactive API docs at `/docs`

**Job API Integrations:**
- ✅ AWS/Amazon Jobs - Real API working perfectly
- ✅ Indeed Jobs - Real API via RapidAPI JSearch
- ✅ LinkedIn Jobs - Real API via RapidAPI JSearch
- ✅ Glassdoor Jobs - Real API via RapidAPI JSearch
- ✅ ZipRecruiter Jobs - Real API via RapidAPI JSearch
- ✅ Netflix Jobs - Available through Indeed/LinkedIn
- ✅ Microsoft Jobs - Available through Indeed/LinkedIn
- ✅ All tech companies - Available through job aggregators

**Security & Infrastructure:**
- Secure API key management with .env
- Git repository with proper .gitignore
- Comprehensive documentation
- Working on both Mac (iOS) and Linux (backend)

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

### High Priority (Ready to Implement)
- [ ] Test resume upload with real PDF in iOS app
- [ ] Implement actual keyword matching algorithm for match percentage
- [ ] Add clearance level selector to iOS search view
- [ ] Store uploaded resumes in backend/database
- [ ] Improve match calculation with weighted scoring

### Medium Priority
- [ ] Integrate AWS Bedrock for AI-powered resume suggestions
- [ ] Add user authentication and accounts
- [ ] Implement job bookmarking/favorites
- [ ] Add filters: location, salary, remote/hybrid
- [ ] Create resume storage (S3 or local database)
- [ ] Add more company integrations (Oracle, L3Harris, OpenAI)

### Low Priority
- [ ] Add unit tests
- [ ] Implement rate limiting
- [ ] Email notifications for new matches
- [ ] Export resume suggestions as PDF
- [ ] Dark mode support
- [ ] iPad optimization

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

### Session 2 (Jan 20, 2026 - Evening)
- Added secure API key management with python-dotenv
- Integrated RapidAPI JSearch for Indeed/LinkedIn/Glassdoor jobs
- Fixed urllib3 compatibility for old OpenSSL
- Successfully tested with real job data ✅
- LinkedIn, Indeed, Glassdoor, ZipRecruiter all working
- API key secured in .env (not committed to Git)
- Resolved git authentication issues
- Copied changes to ~/testing-app/AppleSauce
- Successfully pushed all changes to GitHub ✅

### Session 3 (Jan 20, 2026 - Late Evening)
- Confirmed working on Linux environment (not Mac)
- Backend fully functional with real job APIs
- Identified iOS app testing requires Mac with Xcode
- Web preview available for UI testing on Linux
- All code committed and pushed to GitHub

### Session 4 (Jan 20, 2026 - Night - Mac with Xcode)
- Successfully set up iOS app in Xcode on Mac
- Fixed Swift 6 compatibility issues (@unchecked Sendable)
- iOS app running in simulator with real job data ✅
- Added Dashboard view as new home page
- Implemented Job Search with circular match indicators
- Added security clearance filtering to backend
- Updated tab navigation (Dashboard, Search, Jobs, Upload)
- Match percentage shows green (>50%), red (<50%), yellow (50%)
- Backend clearance endpoint: GET /jobs/clearance?level=secret
- All features tested and working in iOS simulator

### Current Status (End of Day)
- ✅ iOS app fully functional on Mac with Xcode
- ✅ Dashboard with stats, recent jobs, quick actions
- ✅ Job search with visual match indicators
- ✅ Security clearance filtering (None, Confidential, Secret, Top Secret)
- ✅ Real job data from LinkedIn, Indeed, Glassdoor, AWS
- ✅ All code committed and ready to push to GitHub
- 🔜 Ready to continue development tomorrow

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
