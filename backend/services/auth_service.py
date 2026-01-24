"""Authentication service for Google OAuth and JWT tokens"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import requests

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/auth/callback")


class AuthService:
    """Handles authentication operations"""

    def __init__(self):
        self.google_client_id = GOOGLE_CLIENT_ID
        self.google_client_secret = GOOGLE_CLIENT_SECRET
        self.google_redirect_uri = GOOGLE_REDIRECT_URI

    def is_google_configured(self) -> bool:
        """Check if Google OAuth is properly configured"""
        return bool(self.google_client_id and self.google_client_secret)

    def get_google_auth_url(self, state: str = "") -> str:
        """Generate Google OAuth authorization URL"""
        if not self.is_google_configured():
            return ""

        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.google_client_id,
            "redirect_uri": self.google_redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }
        if state:
            params["state"] = state

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{query}"

    def exchange_google_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for tokens and user info"""
        if not self.is_google_configured():
            return None

        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "redirect_uri": self.google_redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()

            # Get user info
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            userinfo_response = requests.get(userinfo_url, headers=headers)
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()

            return {
                "google_id": user_info.get("id"),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "picture_url": user_info.get("picture"),
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
            }

        except requests.RequestException as e:
            print(f"Google OAuth error: {e}")
            return None

    def create_access_token(self, user_id: int, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {
                "user_id": int(payload.get("sub")),
                "email": payload.get("email"),
            }
        except JWTError as e:
            print(f"Token verification failed: {e}")
            return None


# Singleton instance
auth_service = AuthService()
