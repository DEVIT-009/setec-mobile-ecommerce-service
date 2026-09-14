from typing import Optional
from domain.support_ticket.entity.support_ticket import SupportTicket as DomainSupportTicket, SupportMessage as DomainSupportMessage
from infrastructure.persistence.models.support_model import (
    SupportTicket as SupportTicketModel,
    SupportTicketMessage as SupportTicketMessageModel,
)


class SupportPersistenceMapper:

    @staticmethod
    def message_from_entity(entity: Optional[SupportTicketMessageModel]) -> Optional[DomainSupportMessage]:
        if entity is None:
            return None
        return DomainSupportMessage(
            id=str(entity.id),
            ticket_id=str(entity.ticket_id) if entity.ticket_id else None,
            sender_id=str(entity.sender_id) if entity.sender_id else None,
            body=entity.body,
            attachment_url=entity.attachment_url,
            created_at=entity.created_at,
        )

    @staticmethod
    def message_to_model(domain: DomainSupportMessage, model_instance: Optional[SupportTicketMessageModel] = None) -> SupportTicketMessageModel:
        model = model_instance or SupportTicketMessageModel()
        if domain.ticket_id:
            model.ticket_id = domain.ticket_id
        if domain.sender_id:
            model.sender_id = domain.sender_id
        model.body = domain.body
        model.attachment_url = domain.attachment_url
        return model

    @staticmethod
    def from_entity(entity: Optional[SupportTicketModel]) -> Optional[DomainSupportTicket]:
        if entity is None:
            return None
        return DomainSupportTicket(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            order_id=str(entity.order_id) if entity.order_id else None,
            subject=entity.subject,
            category=entity.category,
            status=entity.status,
            priority=entity.priority,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainSupportTicket, model_instance: Optional[SupportTicketModel] = None) -> SupportTicketModel:
        model = model_instance or SupportTicketModel()
        if domain.user_id:
            model.user_id = domain.user_id
        if domain.order_id:
            model.order_id = domain.order_id
        model.subject = domain.subject
        model.category = domain.category
        model.status = domain.status
        model.priority = domain.priority
        model.deleted_at = domain.deleted_at
        return model
