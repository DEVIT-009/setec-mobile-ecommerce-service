from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class UserServiceInterface(ABC):
    @abstractmethod
    def get_me(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_me(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def get_profile(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_profile(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def get_security_settings(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_security_settings(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def list_sessions(self, user_id: str) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def revoke_session(self, user_id: str, session_id: str) -> None: pass
    @abstractmethod
    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]: pass
    @abstractmethod
    def get_admin_user(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def update_admin_user(self, user_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def block_user(self, user_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def unblock_user(self, user_id: str) -> Dict[str, Any]: pass
