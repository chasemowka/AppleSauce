# AppleSauce

Resume analysis and job matching iOS application.

## Project Structure

- `ios-app/` - Swift/SwiftUI iOS application
- `backend/` - Python FastAPI backend service
- `shared/` - Shared data models and types

## Features

- Resume upload and parsing
- Job posting aggregation from multiple sources
- AI-powered resume-to-job matching
- Personalized resume improvement suggestions
- Direct job posting navigation with enhancement sidebar

## Tech Stack

### iOS App
- Swift + SwiftUI
- Local SQLite for caching

### Backend
- Python + FastAPI
- AWS Lambda + API Gateway (serverless)
- Amazon Bedrock for AI analysis
- S3 for file storage
- DynamoDB for data persistence

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### iOS App
Open `ios-app/AppleSauce.xcodeproj` in Xcode

## Development

This project is in active development for personal use.
