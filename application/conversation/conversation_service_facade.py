from typing import Dict, Any
from domain.conversation.ports.conversation_repository import ConversationRepositoryInterface
from domain.conversation.service.conversation_service import ConversationServiceInterface
from domain.conversation.entity.conversation import Conversation, ConversationMessage
from domain.conversation.exception.conversation_exception import ConversationException
from interface.conversation.serializer.mapper.conversation_controller_mapper import ConversationControllerMapper


class ConversationServiceFacade(ConversationServiceInterface):

    def __init__(self, repo: ConversationRepositoryInterface):
        self.repo = repo

    def list_conversations(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        convs, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": ConversationControllerMapper.to_list_response(convs),
            "total": total,
        }

    def create_conversation(self, user_id: str, data: dict) -> Dict[str, Any]:
        conv = Conversation(
            customer_id=user_id,
            store_id=data.get('store_id'),
            order_id=data.get('order_id'),
            status='open',
        )
        saved = self.repo.create(conv)
        if data.get('initial_message'):
            msg = ConversationMessage(
                conversation_id=saved.id,
                sender_id=user_id,
                message_type='text',
                body=data['initial_message'],
            )
            self.repo.send_message(msg)
        return ConversationControllerMapper.to_response(saved)

    def get_conversation(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        conv = self.repo.get_by_id(conversation_id, user_id)
        if not conv:
            raise ConversationException.not_found()
        return ConversationControllerMapper.to_response(conv)

    def update_conversation(self, user_id: str, conversation_id: str, data: dict) -> Dict[str, Any]:
        conv = self.repo.get_by_id(conversation_id, user_id)
        if not conv:
            raise ConversationException.not_found()
        if 'status' in data:
            conv.status = data['status']
        saved = self.repo.save(conv)
        return ConversationControllerMapper.to_response(saved)

    def list_messages(self, user_id: str, conversation_id: str, page: int = 1, page_size: int = 30) -> Dict[str, Any]:
        conv = self.repo.get_by_id(conversation_id, user_id)
        if not conv:
            raise ConversationException.not_found()
        msgs, total = self.repo.list_messages(conversation_id, page, page_size)
        return {
            "items": ConversationControllerMapper.message_to_list_response(msgs),
            "total": total,
        }

    def send_message(self, user_id: str, conversation_id: str, data: dict) -> Dict[str, Any]:
        conv = self.repo.get_by_id(conversation_id, user_id)
        if not conv:
            raise ConversationException.not_found()
        if not data.get('body') and not data.get('attachment_url'):
            raise ConversationException.empty_message()

        msg = ConversationMessage(
            conversation_id=conversation_id,
            sender_id=user_id,
            message_type=data.get('message_type', 'text'),
            body=data.get('body'),
            attachment_url=data.get('attachment_url'),
        )
        saved = self.repo.send_message(msg)
        return ConversationControllerMapper.message_to_response(saved)

    def mark_message_read(self, user_id: str, message_id: str) -> None:
        self.repo.mark_message_read(message_id)
