# Job API Integration Setup

## Quick Start (Works Without API Key)

The app works immediately with:
- ✅ **AWS/Amazon Jobs** - Direct API access (no key needed)
- ✅ **Netflix Jobs** - Direct API access (no key needed)
- ✅ **Mock Data** - Fallback when APIs unavailable

## Optional: Add Indeed/LinkedIn Data (RapidAPI)

For access to Indeed, LinkedIn, and Glassdoor jobs:

### 1. Sign up for RapidAPI (Free)
- Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- Click "Subscribe to Test"
- Choose **Basic Plan (FREE)** - 2,500 requests/month
- Copy your API key

### 2. Set Environment Variable

**Windows:**
```cmd
set RAPIDAPI_KEY=your_api_key_here
```

**Mac/Linux:**
```bash
export RAPIDAPI_KEY=your_api_key_here
```

### 3. Restart Backend
```bash
python main.py
```

## API Endpoints

### Get Jobs from All Sources
```
GET /jobs?query=python developer&source=all
```

### Get Jobs from Specific Source
```
GET /jobs?query=software engineer&source=indeed
GET /jobs?query=cloud engineer&source=aws
GET /jobs?query=frontend developer&source=netflix
```

### Get Jobs from Specific Company
```
GET /jobs/company/aws?keywords=python
GET /jobs/company/netflix?keywords=backend
GET /jobs/company/microsoft?keywords=cloud
```

## Supported Companies

- ✅ **AWS/Amazon** - Full API integration
- ✅ **Netflix** - Full API integration  
- 🔄 **Microsoft** - Placeholder (API requires auth)
- 🔄 **Oracle** - Placeholder
- 🔄 **L3Harris** - Placeholder
- 🔄 **OpenAI** - Placeholder

## Testing

1. Start backend: `python main.py`
2. Open: `http://127.0.0.1:8000/docs`
3. Try:
   - GET `/jobs?query=python&source=aws`
   - GET `/jobs/company/netflix?keywords=engineer`

## Next Steps

- Add more company integrations
- Implement caching for API responses
- Add rate limiting
- Store jobs in database
