from django.urls import path
from interface.conversation.view.conversation_view import (
    ConversationListView, ConversationDetailView,
    ConversationMessageListView, MessageReadView,
)

urlpatterns = [
    path('', ConversationListView.as_view(), name='conversation-list'),
    path('<uuid:conversation_id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('<uuid:conversation_id>/messages/', ConversationMessageListView.as_view(), name='conversation-messages'),
]

message_urlpatterns = [
    path('<uuid:message_id>/read/', MessageReadView.as_view(), name='message-read'),
]
