from django.urls import path
from interface.conversation.view.conversation_view import MessageReadView

urlpatterns = [
    path('<str:message_id>/read/', MessageReadView.as_view(), name='message-read'),
]
