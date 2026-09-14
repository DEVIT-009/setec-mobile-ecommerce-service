from typing import Dict, Any, List
from dataclasses import asdict
from domain.conversation.entity.conversation import Conversation, ConversationMessage
from interface.conversation.serializer.response.conversation_response import (
    ConversationResponse,
    ConversationMessageResponse,
)


class ConversationControllerMapper:

    @staticmethod
    def to_response(conv: Conversation) -> Dict[str, Any]:
        response_dto = ConversationResponse(
            id=str(conv.id) if conv.id else None,
            customer_id=str(conv.customer_id) if conv.customer_id else None,
            store_id=str(conv.store_id) if conv.store_id else None,
            order_id=str(conv.order_id) if conv.order_id else None,
            status=conv.status,
            last_message_at=conv.last_message_at.isoformat() if conv.last_message_at else None,
            created_at=conv.created_at.isoformat() if conv.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(convs: List[Conversation]) -> List[Dict[str, Any]]:
        return [ConversationControllerMapper.to_response(c) for c in convs]

    @staticmethod
    def message_to_response(msg: ConversationMessage) -> Dict[str, Any]:
        response_dto = ConversationMessageResponse(
            id=str(msg.id) if msg.id else None,
            conversation_id=str(msg.conversation_id) if msg.conversation_id else None,
            sender_id=str(msg.sender_id) if msg.sender_id else None,
            message_type=msg.message_type,
            body=msg.body,
            attachment_url=msg.attachment_url,
            read_at=msg.read_at.isoformat() if msg.read_at else None,
            created_at=msg.created_at.isoformat() if msg.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def message_to_list_response(msgs: List[ConversationMessage]) -> List[Dict[str, Any]]:
        return [ConversationControllerMapper.message_to_response(m) for m in msgs]

