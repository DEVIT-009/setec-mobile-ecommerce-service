from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class UserProfileResponse:
    date_of_birth: Optional[Any] = None
    gender: Optional[str] = None
    preferred_language: Optional[str] = None
    marketing_opt_in: Optional[bool] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class UserSecurityResponse:
    two_factor_enabled: Optional[bool] = None
    biometric_enabled: Optional[bool] = None
    last_password_changed_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class UserSessionResponse:
    id: Optional[str] = None
    device_name: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    last_seen_at: Optional[str] = None
    revoked_at: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class UserResponse:
    id: Optional[str]
    email: str
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    email_verified_at: Optional[str] = None
    phone_verified_at: Optional[str] = None
    profile: Optional[Dict[str, Any]] = None
    security_settings: Optional[Dict[str, Any]] = None
    default_address: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
