from django.urls import path
from interface.support_ticket.view.support_ticket_view import (
    SupportTicketListView,
    SupportTicketDetailView,
    SupportTicketMessageListView,
)

urlpatterns = [
    path('tickets/', SupportTicketListView.as_view(), name='support-ticket-list'),
    path('tickets/<uuid:ticket_id>/', SupportTicketDetailView.as_view(), name='support-ticket-detail'),
    path('tickets/<uuid:ticket_id>/messages/', SupportTicketMessageListView.as_view(), name='support-ticket-messages'),
]
