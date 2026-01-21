# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppleSauce is a resume analysis and job matching application with a native iOS frontend and Python FastAPI backend. Users upload resumes, browse job postings from multiple sources, and receive AI-scored job matches with resume improvement suggestions.

## Tech Stack

- **iOS App**: Swift 6 + SwiftUI, iOS 14+, no external dependencies
- **Backend**: Python 3.7+ with FastAPI, Uvicorn
- **Job APIs**: AWS Jobs (direct), Indeed/LinkedIn/Glassdoor (via RapidAPI JSearch)

## Commands

### Backend Development
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
python main.py                 # Starts server at http://127.0.0.1:8000
```

### API Testing
```bash
# Interactive docs
http://127.0.0.1:8000/docs

# Manual testing
curl http://127.0.0.1:8000/jobs?query=python&source=all
curl http://127.0.0.1:8000/jobs/company/aws?keywords=developer
curl -X POST http://127.0.0.1:8000/upload-resume -F "file=@resume.pdf"
```

### iOS App (Mac with Xcode only)
1. Open Xcode and create new iOS App project
2. Add Swift files from `ios-app/AppleSauce/AppleSauce/`
3. Add network permission to Info.plist: `NSAllowsLocalNetworking = true`
4. Run in simulator (Cmd+R)

### Web Preview (for testing on non-Mac)
```bash
cd web-preview
python -m http.server 8080    # http://localhost:8080
```

## Architecture

### iOS Structure
```
AppleSauceApp.swift     → App entry point (@main)
ContentView.swift       → Root TabView (Dashboard, Resume, Jobs)
APIService.swift        → Network layer (static methods, URLSession)
Models.swift            → Resume and Job data models
DashboardView.swift     → Home page with stats
JobSearchView.swift     → Search with circular match % indicators
JobListingsView.swift   → Job list with navigation
JobDetailView.swift     → Job details + suggestions sidebar
```

**State management**: SwiftUI @State/@Binding, DispatchQueue.main.async for UI updates

### Backend Structure
```
main.py                       → FastAPI app with 6 endpoints
services/
  job_api_service.py          → Multi-source job fetching (262 lines)
  resume_parser.py            → PDF/DOCX parsing
  job_matcher.py              → Resume-to-job matching algorithm
  clearance_filter.py         → Security clearance filtering
```

**Data flow**: iOS → APIService (multipart/form-data) → FastAPI → JSON response

### API Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/upload-resume` | Parse PDF/DOCX resume |
| GET | `/jobs` | Search jobs (params: query, source) |
| GET | `/jobs/company/{company}` | Company-specific jobs |
| GET | `/jobs/clearance` | Filter by clearance level |
| POST | `/match` | Score job matches against resume |
| POST | `/suggestions` | Get resume improvement suggestions |

## Key Patterns

- **Swift 6 compatibility**: Use `@unchecked Sendable` where needed
- **API keys**: Store in `.env` file (use python-dotenv), never commit
- **Backend localhost**: Use `127.0.0.1` not `localhost` on Windows
- **Design system**: Colors in `DesignSystem/Colors.swift`, typography in `Typography.swift`
- **Match indicators**: Green (>50%), yellow (50%), red (<50%)

## Environment Setup

For RapidAPI JSearch (Indeed/LinkedIn/Glassdoor):
1. Get free key at https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Create `backend/.env` with `RAPIDAPI_KEY=your_key_here`
