from typing import Dict, Any, List, Optional
from dataclasses import asdict
from domain.user.entity.user import User, UserProfile, UserSecuritySettings, UserSession
from interface.user.serializer.response.user_response import (
    UserResponse,
    UserProfileResponse,
    UserSecurityResponse,
    UserSessionResponse,
)


class UserControllerMapper:

    @staticmethod
    def to_user_response(
        user: User,
        profile: Optional[UserProfile] = None,
        security: Optional[UserSecuritySettings] = None,
        default_address: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        response_dto = UserResponse(
            id=str(user.id) if user.id else None,
            email=user.email,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar_url=user.avatar_url,
            role=user.role,
            status=user.status,
            email_verified_at=user.email_verified_at.isoformat() if user.email_verified_at else None,
            phone_verified_at=user.phone_verified_at.isoformat() if user.phone_verified_at else None,
            profile=UserControllerMapper.to_profile_response(profile) if profile else None,
            security_settings=UserControllerMapper.to_security_response(security) if security else None,
            default_address=default_address,
            created_at=user.created_at.isoformat() if user.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_profile_response(profile: UserProfile) -> Dict[str, Any]:
        response_dto = UserProfileResponse(
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            preferred_language=profile.preferred_language,
            marketing_opt_in=profile.marketing_opt_in,
        )
        return asdict(response_dto)

    @staticmethod
    def to_security_response(security: UserSecuritySettings) -> Dict[str, Any]:
        response_dto = UserSecurityResponse(
            two_factor_enabled=security.two_factor_enabled,
            biometric_enabled=security.biometric_enabled,
            last_password_changed_at=security.last_password_changed_at.isoformat() if security.last_password_changed_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_session_response(session: UserSession) -> Dict[str, Any]:
        response_dto = UserSessionResponse(
            id=str(session.id) if session.id else None,
            device_name=session.device_name,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            last_seen_at=session.last_seen_at.isoformat() if session.last_seen_at else None,
            revoked_at=session.revoked_at.isoformat() if session.revoked_at else None,
            created_at=session.created_at.isoformat() if session.created_at else None,
        )
        return asdict(response_dto)

