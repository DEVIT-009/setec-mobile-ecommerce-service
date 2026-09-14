from typing import List, Optional, Tuple
from django.utils import timezone
from domain.conversation.ports.conversation_repository import ConversationRepositoryInterface
from domain.conversation.entity.conversation import Conversation, ConversationMessage
from infrastructure.persistence.mapper.conversation_persistence_mapper import ConversationPersistenceMapper
from infrastructure.persistence.models.conversation_model import (
    Conversation as ConversationModel,
    Message as MessageModel,
)


class ConversationRepositoryInterfaceImpl(ConversationRepositoryInterface):

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Conversation], int]:
        qs = ConversationModel.objects.filter(customer_id=user_id, deleted_at__isnull=True).order_by('-last_message_at', '-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ConversationPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def create(self, conv: Conversation) -> Conversation:
        model = ConversationPersistenceMapper.to_model(conv)
        model.save()
        return ConversationPersistenceMapper.from_entity(model)

    def get_by_id(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        model = ConversationModel.objects.filter(id=conversation_id, customer_id=user_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return ConversationPersistenceMapper.from_entity(model)

    def save(self, conv: Conversation) -> Conversation:
        db_instance = ConversationModel.objects.filter(pk=conv.id).first() if conv.id else None
        db_instance = ConversationPersistenceMapper.to_model(conv, db_instance)
        db_instance.save()
        return ConversationPersistenceMapper.from_entity(db_instance)

    def list_messages(self, conversation_id: str, page: int, page_size: int) -> Tuple[List[ConversationMessage], int]:
        qs = MessageModel.objects.filter(conversation_id=conversation_id, deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ConversationPersistenceMapper.message_from_entity(m) for m in models if m is not None], total

    def send_message(self, msg: ConversationMessage) -> ConversationMessage:
        model = ConversationPersistenceMapper.message_to_model(msg)
        model.save()
        # update conversation last_message_at
        ConversationModel.objects.filter(id=msg.conversation_id).update(last_message_at=timezone.now())
        return ConversationPersistenceMapper.message_from_entity(model)

    def mark_message_read(self, message_id: str) -> None:
        MessageModel.objects.filter(id=message_id, read_at__isnull=True).update(read_at=timezone.now())
