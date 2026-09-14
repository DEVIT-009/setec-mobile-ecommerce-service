from rest_framework import serializers

NOTIFICATION_TYPE_CHOICES = ['order', 'promotion', 'system', 'review', 'support']


class AdminSendNotificationRequest(serializers.Serializer):
    user_id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=NOTIFICATION_TYPE_CHOICES)
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(required=False, allow_blank=True)
    data = serializers.DictField(required=False)


# Backward-compatibility alias
AdminSendNotificationSerializer = AdminSendNotificationRequest
