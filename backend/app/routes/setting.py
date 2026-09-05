from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password, verify_password, get_current_user, oauth2_scheme
from jose import jwt

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

# Pydantic models
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class NotificationSettings(BaseModel):
    email_notifications: bool = True
    push_notifications: bool = True
    new_releases: bool = True
    playlist_updates: bool = True
    social_activity: bool = False
    marketing_emails: bool = False

class PlaybackSettings(BaseModel):
    crossfade: bool = False
    gapless_playback: bool = True
    auto_play: bool = True
    streaming_quality: str = "high"
    download_quality: str = "high"
    normalize_volume: bool = True

class PreferencesSettings(BaseModel):
    language: str = "en"
    region: str = "US"
    theme: str = "dark"

class UserSettingsResponse(BaseModel):
    user_id: int
    name: str
    username: str
    email: EmailStr
    profile_image: Optional[str] = None
    notifications: NotificationSettings
    playback: PlaybackSettings
    preferences: PreferencesSettings
    two_factor_enabled: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

# In-memory storage for settings (in production, use a database table)
user_settings_store = {}

def get_user_settings(user_id: int) -> dict:
    """Get user settings from store or return defaults"""
    if user_id not in user_settings_store:
        user_settings_store[user_id] = {
            "notifications": NotificationSettings().dict(),
            "playback": PlaybackSettings().dict(),
            "preferences": PreferencesSettings().dict(),
            "two_factor_enabled": False
        }
    return user_settings_store[user_id]

@router.get("/profile", response_model=UserSettingsResponse)
def get_profile(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile with settings"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)

    return UserSettingsResponse(
        user_id=user.user_id,
        name=user.name,
        username=user.username,
        email=user.email,
        profile_image=user.profile_image,
        notifications=NotificationSettings(**settings["notifications"]),
        playback=PlaybackSettings(**settings["playback"]),
        preferences=PreferencesSettings(**settings["preferences"]),
        two_factor_enabled=settings["two_factor_enabled"],
        created_at=datetime.utcnow()
    )

@router.put("/profile")
def update_profile(
    profile_data: ProfileUpdate,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if profile_data.name is not None:
        user.name = profile_data.name
    if profile_data.username is not None:
        # Check if username is already taken
        existing = db.query(User).filter(User.username == profile_data.username).first()
        if existing and existing.user_id != user.user_id:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = profile_data.username

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "username": user.username,
            "email": user.email
        }
    }

@router.put("/password")
def change_password(
    password_data: PasswordChange,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password_data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if len(password_data.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")

    user.password = hash_password(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}

@router.get("/notifications", response_model=NotificationSettings)
def get_notification_settings(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification settings"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    return NotificationSettings(**settings["notifications"])

@router.put("/notifications")
def update_notification_settings(
    settings_data: NotificationSettings,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update notification settings"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    settings["notifications"] = settings_data.dict()

    return {"message": "Notification settings updated successfully", "settings": settings_data}

@router.get("/playback", response_model=PlaybackSettings)
def get_playback_settings(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get playback settings"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    return PlaybackSettings(**settings["playback"])

@router.put("/playback")
def update_playback_settings(
    settings_data: PlaybackSettings,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update playback settings"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    settings["playback"] = settings_data.dict()

    return {"message": "Playback settings updated successfully", "settings": settings_data}

@router.get("/preferences", response_model=PreferencesSettings)
def get_preferences(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    return PreferencesSettings(**settings["preferences"])

@router.put("/preferences")
def update_preferences(
    settings_data: PreferencesSettings,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    settings = get_user_settings(user.user_id)
    settings["preferences"] = settings_data.dict()

    return {"message": "Preferences updated successfully", "settings": settings_data}

@router.delete("/account")
def delete_account(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.user_id
    db.delete(user)
    db.commit()

    # Clean up settings store
    if user_id in user_settings_store:
        del user_settings_store[user_id]

    return {"message": "Account deleted successfully"}