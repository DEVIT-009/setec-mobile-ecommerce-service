from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from domain.legal_document.entity.legal_document import LegalDocument, LegalAcceptance

class LegalRepositoryInterface(ABC):
    @abstractmethod
    def list_published(self, doc_type: Optional[str] = None) -> List[LegalDocument]: pass
    @abstractmethod
    def get_latest_by_type(self, doc_type: str) -> Optional[LegalDocument]: pass
    @abstractmethod
    def get_by_id(self, doc_id: str) -> Optional[LegalDocument]: pass
    @abstractmethod
    def record_acceptance(self, acceptance: LegalAcceptance) -> LegalAcceptance: pass
    @abstractmethod
    def list_acceptances(self, user_id: str) -> List[LegalAcceptance]: pass
