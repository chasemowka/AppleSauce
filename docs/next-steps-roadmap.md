# AppleSauce Project Roadmap & Strategy

## Phase 1: Foundation Cleanup & Reliability
**Goal:** Transition from a prototype with "filler data" to a production-ready application that fails gracefully and displays only real data.

### 1.1 Backend: Remove Filler/Mock Data
- **Strategy:** Adopt a "Fail Loud" or "Empty State" approach.
- **Action Items:**
  - Remove `_get_mock_jobs` from `job_api_service.py`.
  - Refactor `search_indeed_jobs` and `search_company_careers` to return empty lists `[]` on API failure instead of mock objects.
  - Ensure `.env` loading is robust; log warnings if keys are missing but do not inject fake data.

### 1.2 Frontend (Web Preview): UI Cleanup
- **Strategy:** Modernize the "Web Preview" to match the "Premium Design" aesthetic of the iOS app.
- **Action Items:**
  - Remove hardcoded HTML job cards in `index.html`.
  - Implement a JavaScript fetcher to load jobs dynamically from `http://127.0.0.1:8000/jobs`.
  - Handle empty states gracefully (e.g., "No jobs found for your search").
  - Improve CSS: Use system fonts, better padding/margins, and subtle shadows.

## Phase 2: Resume Intelligence (Scraping/Parsing)
**Goal:** Transform the resume parser from a simple text dumper into a structured data extractor.

### 2.1 Structured Parsing
- **Strategy:** Extract semantic meaning, not just strings.
- **Action Items:**
  - Enhance `resume_parser.py` to identify and separate sections:
    - **Skills**: Look for headers like "Skills", "Technologies", "Stack".
    - **Experience**: Look for date ranges and job titles.
    - **Education**: Extract degrees and universities.
  - Return a JSON object (or Dictionary) from `/upload-resume`:
    ```json
    {
      "text": "Full raw text...",
      "skills": ["Python", "Swift", "AWS"],
      "experience_years": 5,
      "sections": { ... }
    }
    ```

### 2.2 Intelligent Matching
- **Strategy:** Match based on *Skills* overlap, not just keyword occurrence in the blob.
- **Action Items:**
  - Update `job_matcher.py` to compare `resume.skills` against `job.skills`.
  - Implement a weighted scoring system:
    - 50% for Skill match
    - 30% for Title match
    - 20% for raw keyword overlap

## Phase 3: Identity & Personalization
**Goal:** Allow users to save their data and preferences via extensive Google Login integration.

### 3.1 Authentication
- **Strategy:** Use OAuth 2.0 for secure, password-less login.
- **Action Items:**
  - **Backend**:
    - Install `google-auth` / `requests`.
    - Create `auth_service.py`.
    - Implement endpoints: `GET /auth/login` (returns redirect URL) and `GET /auth/callback` (exchanges code for token).
  - **Frontend**:
    - Add "Sign in with Google" button.
    - Store JWT/Session token in LocalStorage (Web) or Keychain (iOS).

## Phase 4: Verification & Polish
**Strategy:** Validate against real-world scenarios.

1. **Empty State Test**: Run app with NO internet/API keys. application should show "0 Jobs" cleanly.
2. **Parsing Test**: Upload 3 different resume formats (Standard PDF, Creative PDF, DOCX). Verify extracted skills match reality.
3. **Login Test**: Authenticate via Google and verify user profile is returned.
