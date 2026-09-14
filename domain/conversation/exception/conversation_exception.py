from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class ConversationException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Conversation not found", "CONVERSATION_NOT_FOUND")

    @classmethod
    def message_not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "Message not found", "MESSAGE_NOT_FOUND")
