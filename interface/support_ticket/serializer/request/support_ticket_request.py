from rest_framework import serializers

TICKET_CATEGORY_CHOICES = ['order', 'payment', 'delivery', 'account', 'other']
TICKET_STATUS_CHOICES = ['open', 'in_progress', 'resolved', 'closed']
TICKET_PRIORITY_CHOICES = ['low', 'normal', 'high', 'urgent']


class CreateTicketRequest(serializers.Serializer):
    subject = serializers.CharField(max_length=500)
    category = serializers.ChoiceField(choices=TICKET_CATEGORY_CHOICES, default='other')
    priority = serializers.ChoiceField(choices=TICKET_PRIORITY_CHOICES, default='normal', required=False)
    order_id = serializers.CharField(required=False, allow_null=True)
    message = serializers.CharField(required=False, allow_blank=True)


class UpdateTicketRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=TICKET_STATUS_CHOICES, required=False)
    priority = serializers.ChoiceField(choices=TICKET_PRIORITY_CHOICES, required=False)


class AddTicketMessageRequest(serializers.Serializer):
    body = serializers.CharField()


class AdminUpdateTicketRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=TICKET_STATUS_CHOICES, required=False)
    priority = serializers.ChoiceField(choices=TICKET_PRIORITY_CHOICES, required=False)
    assigned_to = serializers.CharField(required=False, allow_null=True)


class AdminReplyTicketRequest(serializers.Serializer):
    body = serializers.CharField()


# Backward-compatibility aliases
CreateTicketSerializer = CreateTicketRequest
UpdateTicketSerializer = UpdateTicketRequest
AddTicketMessageSerializer = AddTicketMessageRequest
AdminUpdateTicketSerializer = AdminUpdateTicketRequest
AdminReplyTicketSerializer = AdminReplyTicketRequest
