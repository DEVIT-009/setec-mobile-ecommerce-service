from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AuthServiceInterface(ABC):
    @abstractmethod
    def register(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None, phone_number: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def login(self, email: str, password: str, request: Any = None) -> Dict[str, Any]: pass
    @abstractmethod
    def get_me(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def logout(self, user_id: str, session_id: Optional[str] = None) -> None: pass
    @abstractmethod
    def refresh(self, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def forgot_password(self, email: str) -> Dict[str, Any]: pass
    @abstractmethod
    def reset_password(self, reset_token: str, new_password: str) -> Dict[str, Any]: pass
    @abstractmethod
    def verify_email(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def verify_phone(self, user_id: str, phone_number: Optional[str] = None) -> Dict[str, Any]: pass
