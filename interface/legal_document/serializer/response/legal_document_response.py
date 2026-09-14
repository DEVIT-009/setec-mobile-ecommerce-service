from dataclasses import dataclass
from typing import Optional


@dataclass
class LegalDocumentResponse:
    id: Optional[str]
    type: str
    title: str
    version: str
    content: str
    status: str
    published_at: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class LegalAcceptanceResponse:
    id: Optional[str]
    legal_document_id: Optional[str]
    user_id: Optional[str]
    accepted_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
