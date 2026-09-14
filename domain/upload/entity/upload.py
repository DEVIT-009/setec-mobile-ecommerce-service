from dataclasses import dataclass
from typing import Optional

@dataclass
class CloudinarySignature:
    api_key: str = ""
    timestamp: int = 0
    signature: str = ""
    cloud_name: str = ""
    folder: str = ""
    upload_preset: Optional[str] = None

@dataclass
class CloudinaryAsset:
    public_id: str = ""
    url: str = ""
    secure_url: str = ""
    mime_type: Optional[str] = None
    size: Optional[int] = None
    usage_type: Optional[str] = None
