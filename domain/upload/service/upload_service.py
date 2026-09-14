from abc import ABC, abstractmethod
from typing import Dict, Any

class UploadServiceInterface(ABC):
    @abstractmethod
    def generate_signature(self, folder: str = "uploads") -> Dict[str, Any]: pass
    @abstractmethod
    def confirm_upload(self, user_id: str, data: dict) -> Dict[str, Any]: pass
