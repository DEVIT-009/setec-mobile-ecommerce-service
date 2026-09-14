from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LegalDocument:
    id: Optional[str] = None
    type: str = ""
    title: str = ""
    version: str = ""
    content: str = ""
    published_at: Optional[datetime] = None
    status: str = "draft"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class LegalAcceptance:
    id: Optional[str] = None
    user_id: Optional[str] = None
    legal_document_id: Optional[str] = None
    document_type: Optional[str] = None
    document_version: Optional[str] = None
    accepted_at: Optional[datetime] = None
    ip_address: Optional[str] = None
