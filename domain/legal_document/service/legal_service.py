from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LegalServiceInterface(ABC):
    @abstractmethod
    def list_published(self, doc_type: Optional[str] = None) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def get_latest_by_type(self, doc_type: str) -> Dict[str, Any]: pass
    @abstractmethod
    def accept(self, user_id: str, doc_id: str, ip_address: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def list_user_acceptances(self, user_id: str) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def list_admin_versions(self, doc_type: Optional[str] = None) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def create_admin_version(self, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def update_admin_version(self, doc_id: str, data: dict) -> Dict[str, Any]: pass
    @abstractmethod
    def publish_admin_version(self, doc_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def archive_admin_version(self, doc_id: str) -> Dict[str, Any]: pass
