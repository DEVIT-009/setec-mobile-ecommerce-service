from typing import Dict, Any, List
from dataclasses import asdict
from domain.legal_document.entity.legal_document import LegalDocument, LegalAcceptance
from interface.legal_document.serializer.response.legal_document_response import (
    LegalDocumentResponse,
    LegalAcceptanceResponse,
)


class LegalControllerMapper:

    @staticmethod
    def to_response(doc: LegalDocument) -> Dict[str, Any]:
        response_dto = LegalDocumentResponse(
            id=str(doc.id) if doc.id else None,
            type=doc.type,
            title=doc.title,
            version=doc.version,
            content=doc.content,
            status=doc.status,
            published_at=doc.published_at.isoformat() if doc.published_at else None,
            created_at=doc.created_at.isoformat() if doc.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(docs: List[LegalDocument]) -> List[Dict[str, Any]]:
        return [LegalControllerMapper.to_response(d) for d in docs]

    @staticmethod
    def acceptance_to_response(acc: LegalAcceptance) -> Dict[str, Any]:
        response_dto = LegalAcceptanceResponse(
            id=str(acc.id) if acc.id else None,
            legal_document_id=str(acc.legal_document_id) if acc.legal_document_id else None,
            user_id=str(acc.user_id) if acc.user_id else None,
            accepted_at=acc.accepted_at.isoformat() if acc.accepted_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def acceptance_to_list_response(accs: List[LegalAcceptance]) -> List[Dict[str, Any]]:
        return [LegalControllerMapper.acceptance_to_response(a) for a in accs]

