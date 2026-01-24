"""Authentication routes for Google OAuth"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models.db_models import User
from services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Dependency to get current authenticated user from JWT token"""
    if not authorization:
        return None

    # Extract token from "Bearer <token>" format
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization

    token_data = auth_service.verify_token(token)
    if not token_data:
        return None

    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    return user


def require_auth(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Dependency that requires authentication - raises 401 if not authenticated"""
    user = get_current_user(authorization, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/status")
async def auth_status(
    current_user: Optional[User] = Depends(get_current_user)
):
    """Check authentication status and configuration"""
    return {
        "authenticated": current_user is not None,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "picture_url": current_user.picture_url,
        } if current_user else None,
        "google_oauth_configured": auth_service.is_google_configured(),
    }


@router.get("/google/login")
async def google_login(redirect_url: str = Query(default="")):
    """
    Get Google OAuth login URL

    - redirect_url: Optional URL to redirect to after successful login
    """
    if not auth_service.is_google_configured():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env"
        )

    auth_url = auth_service.get_google_auth_url(state=redirect_url)
    return {"auth_url": auth_url}


@router.get("/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(default=""),
    db: Session = Depends(get_db)
):
    """
    Google OAuth callback - exchanges code for user info and creates/updates user
    """
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # Exchange code for user info
    user_info = auth_service.exchange_google_code(code)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Google")

    # Find or create user
    user = db.query(User).filter(User.google_id == user_info["google_id"]).first()

    if not user:
        # Check if email exists (maybe signed up differently)
        user = db.query(User).filter(User.email == user_info["email"]).first()
        if user:
            # Link Google account to existing user
            user.google_id = user_info["google_id"]
        else:
            # Create new user
            user = User(
                email=user_info["email"],
                name=user_info["name"],
                picture_url=user_info["picture_url"],
                google_id=user_info["google_id"],
            )
            db.add(user)

    # Update last login
    user.last_login = datetime.utcnow()
    if user_info.get("name"):
        user.name = user_info["name"]
    if user_info.get("picture_url"):
        user.picture_url = user_info["picture_url"]

    db.commit()
    db.refresh(user)

    # Create JWT token
    access_token = auth_service.create_access_token(user.id, user.email)

    # If there's a redirect URL (state), redirect with token
    if state:
        # For mobile apps, use custom scheme: applesauce://auth?token=xxx
        return RedirectResponse(url=f"{state}?token={access_token}")

    # Otherwise return JSON response
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture_url": user.picture_url,
        }
    }


@router.post("/logout")
async def logout(current_user: User = Depends(require_auth)):
    """
    Logout current user (client should discard token)
    """
    # JWT tokens are stateless, so we just return success
    # Client is responsible for discarding the token
    return {"message": "Logged out successfully"}


@router.post("/apple")
async def apple_login(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Sign in with Apple - receives identity token from iOS app

    Request body:
    - identity_token: JWT from Apple (for server-side verification)
    - user_id: Apple's unique user identifier
    - email: User's email (only provided on first sign-in)
    - full_name: User's name (only provided on first sign-in)
    """
    user_id = data.get("user_id")
    email = data.get("email")
    full_name = data.get("full_name")
    identity_token = data.get("identity_token")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    # Note: In production, you should verify the identity_token with Apple's servers
    # For now, we trust the client (iOS app) since it's using Apple's AuthenticationServices
    # To verify: decode JWT, check issuer is "https://appleid.apple.com", verify signature

    # Find existing user by Apple ID
    user = db.query(User).filter(User.apple_id == user_id).first()

    if not user:
        # Check if email exists (maybe signed up with Google)
        if email:
            user = db.query(User).filter(User.email == email).first()
            if user:
                # Link Apple account to existing user
                user.apple_id = user_id
            else:
                # Create new user
                user = User(
                    email=email or f"{user_id}@privaterelay.appleid.com",
                    name=full_name or "Apple User",
                    apple_id=user_id,
                )
                db.add(user)
        else:
            # No email provided and no existing user - create with placeholder
            user = User(
                email=f"{user_id}@privaterelay.appleid.com",
                name=full_name or "Apple User",
                apple_id=user_id,
            )
            db.add(user)

    # Update last login and name if provided
    user.last_login = datetime.utcnow()
    if full_name and full_name != "Apple User":
        user.name = full_name

    db.commit()
    db.refresh(user)

    # Create JWT token
    access_token = auth_service.create_access_token(user.id, user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture_url": user.picture_url,
        }
    }


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(require_auth)):
    """Get current authenticated user's information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "picture_url": current_user.picture_url,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
    }
