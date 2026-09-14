from dataclasses import dataclass
from typing import Optional


@dataclass
class CloudinarySignatureResponse:
    timestamp: int
    signature: str
    api_key: str
    cloud_name: str
    folder: str

    def to_dict(self):
        return self.__dict__


@dataclass
class UploadResponse:
    id: Optional[str]
    user_id: Optional[str]
    public_id: str
    url: str
    secure_url: Optional[str] = None
    mime_type: Optional[str] = None
    usage_type: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
