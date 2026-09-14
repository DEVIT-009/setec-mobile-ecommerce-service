from typing import Dict, Any, List
from dataclasses import asdict
from domain.support_ticket.entity.support_ticket import SupportTicket, SupportMessage
from interface.support_ticket.serializer.response.support_ticket_response import (
    SupportTicketResponse,
    SupportMessageResponse,
)


class SupportControllerMapper:

    @staticmethod
    def to_response(ticket: SupportTicket) -> Dict[str, Any]:
        response_dto = SupportTicketResponse(
            id=str(ticket.id) if ticket.id else None,
            user_id=str(ticket.user_id) if ticket.user_id else None,
            order_id=str(ticket.order_id) if ticket.order_id else None,
            subject=ticket.subject,
            category=ticket.category,
            status=ticket.status,
            priority=ticket.priority,
            created_at=ticket.created_at.isoformat() if ticket.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(tickets: List[SupportTicket]) -> List[Dict[str, Any]]:
        return [SupportControllerMapper.to_response(t) for t in tickets]

    @staticmethod
    def message_to_response(msg: SupportMessage) -> Dict[str, Any]:
        response_dto = SupportMessageResponse(
            id=str(msg.id) if msg.id else None,
            ticket_id=str(msg.ticket_id) if msg.ticket_id else None,
            sender_id=str(msg.sender_id) if msg.sender_id else None,
            body=msg.body,
            attachment_url=msg.attachment_url,
            created_at=msg.created_at.isoformat() if msg.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def message_to_list_response(msgs: List[SupportMessage]) -> List[Dict[str, Any]]:
        return [SupportControllerMapper.message_to_response(m) for m in msgs]

