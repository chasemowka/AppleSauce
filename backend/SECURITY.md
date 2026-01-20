# Security Guide - AppleSauce Backend

## API Key Management

This project uses secure environment variable management to protect sensitive API keys.

### Setup Instructions

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   - Get your RapidAPI key from [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
   - Replace `your_rapidapi_key_here` with your actual key

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Security Features

- **Environment Variables**: API keys are stored in `.env` file, not in code
- **Git Protection**: `.env` is excluded from version control via `.gitignore`
- **Template File**: `.env.example` provides setup guidance without exposing keys
- **Automatic Loading**: `python-dotenv` loads environment variables at runtime

### Important Security Notes

⚠️ **Never commit API keys to version control**
- The `.env` file is automatically ignored by Git
- Always use `.env.example` for documentation
- Rotate keys if accidentally exposed

⚠️ **Production Deployment**
- Use your hosting platform's environment variable system
- Never deploy `.env` files to production servers
- Consider using secrets management services for production

### Troubleshooting

If you see "Warning: RAPIDAPI_KEY not set":
1. Ensure `.env` file exists in the backend directory
2. Verify the key is correctly set in `.env`
3. Restart the application after making changes

### Key Rotation

To rotate your API key:
1. Generate a new key in RapidAPI dashboard
2. Update the key in your `.env` file
3. Restart the application
4. Revoke the old key in RapidAPI dashboard