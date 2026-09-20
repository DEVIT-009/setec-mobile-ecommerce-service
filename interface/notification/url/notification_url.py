from django.urls import path
from interface.notification.view.notification_view import (
    NotificationListView, NotificationUnreadCountView,
    NotificationReadAllView, NotificationDetailView, NotificationReadView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', NotificationUnreadCountView.as_view(), name='notification-unread-count'),
    path('read-all/', NotificationReadAllView.as_view(), name='notification-read-all'),
    path('<str:notification_id>/', NotificationDetailView.as_view(), name='notification-delete'),
    path('<str:notification_id>/read/', NotificationReadView.as_view(), name='notification-read'),
]
