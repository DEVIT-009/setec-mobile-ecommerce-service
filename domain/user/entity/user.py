from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[str] = None
    email: str = ""
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "customer"
    status: str = "pending_verification"
    email_verified_at: Optional[datetime] = None
    phone_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

@dataclass
class UserProfile:
    id: Optional[str] = None
    user_id: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    preferred_language: str = "en"
    marketing_opt_in: bool = False
    updated_at: Optional[datetime] = None

@dataclass
class UserSecuritySettings:
    id: Optional[str] = None
    user_id: Optional[str] = None
    two_factor_enabled: bool = False
    biometric_enabled: bool = False
    last_password_changed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class UserSession:
    id: Optional[str] = None
    user_id: Optional[str] = None
    device_name: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
