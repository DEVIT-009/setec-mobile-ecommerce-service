from typing import Optional
from domain.conversation.entity.conversation import Conversation as DomainConversation, ConversationMessage as DomainConversationMessage
from infrastructure.persistence.models.conversation_model import (
    Conversation as ConversationModel,
    Message as MessageModel,
)


class ConversationPersistenceMapper:

    @staticmethod
    def message_from_entity(entity: Optional[MessageModel]) -> Optional[DomainConversationMessage]:
        if entity is None:
            return None
        return DomainConversationMessage(
            id=str(entity.id),
            conversation_id=str(entity.conversation_id) if entity.conversation_id else None,
            sender_id=str(entity.sender_id) if entity.sender_id else None,
            message_type=entity.message_type,
            body=entity.body,
            attachment_url=entity.attachment_url,
            read_at=entity.read_at,
            created_at=entity.created_at,
        )

    @staticmethod
    def message_to_model(domain: DomainConversationMessage, model_instance: Optional[MessageModel] = None) -> MessageModel:
        model = model_instance or MessageModel()
        if domain.conversation_id:
            model.conversation_id = domain.conversation_id
        if domain.sender_id:
            model.sender_id = domain.sender_id
        model.message_type = domain.message_type
        model.body = domain.body
        model.attachment_url = domain.attachment_url
        model.read_at = domain.read_at
        return model

    @staticmethod
    def from_entity(entity: Optional[ConversationModel]) -> Optional[DomainConversation]:
        if entity is None:
            return None
        return DomainConversation(
            id=str(entity.id),
            customer_id=str(entity.customer_id) if entity.customer_id else None,
            store_id=str(entity.store_id) if entity.store_id else None,
            order_id=str(entity.order_id) if entity.order_id else None,
            status=entity.status,
            last_message_at=entity.last_message_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainConversation, model_instance: Optional[ConversationModel] = None) -> ConversationModel:
        model = model_instance or ConversationModel()
        if domain.customer_id:
            model.customer_id = domain.customer_id
        if domain.store_id:
            model.store_id = domain.store_id
        if domain.order_id:
            model.order_id = domain.order_id
        model.status = domain.status
        model.last_message_at = domain.last_message_at
        model.deleted_at = domain.deleted_at
        return model
