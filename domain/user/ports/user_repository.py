from abc import ABC, abstractmethod
from typing import Optional, List
from domain.user.entity.user import User, UserProfile, UserSecuritySettings, UserSession

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]: pass
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: pass
    @abstractmethod
    def save(self, user: User) -> User: pass
    @abstractmethod
    def get_profile(self, user_id: str) -> Optional[UserProfile]: pass
    @abstractmethod
    def save_profile(self, profile: UserProfile) -> UserProfile: pass
    @abstractmethod
    def get_security_settings(self, user_id: str) -> Optional[UserSecuritySettings]: pass
    @abstractmethod
    def save_security_settings(self, settings: UserSecuritySettings) -> UserSecuritySettings: pass
    @abstractmethod
    def list_sessions(self, user_id: str) -> List[UserSession]: pass
    @abstractmethod
    def get_session(self, session_id: str, user_id: str) -> Optional[UserSession]: pass
    @abstractmethod
    def save_session(self, session: UserSession) -> UserSession: pass
