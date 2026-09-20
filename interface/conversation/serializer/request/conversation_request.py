from rest_framework import serializers


class CreateConversationRequest(serializers.Serializer):
    store_id = serializers.CharField(required=False, allow_null=True)
    order_id = serializers.CharField(required=False, allow_null=True)


class SendMessageRequest(serializers.Serializer):
    message_type = serializers.ChoiceField(choices=['text', 'image', 'system'], default='text')
    body = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    attachment_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)

    def validate(self, data):
        if not data.get('body') and not data.get('attachment_url') and data.get('message_type') != 'system':
            raise serializers.ValidationError("Either body or attachment_url is required.")
        return data


class PatchConversationRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=['open', 'closed', 'archived'], required=False)


# Backward-compatibility aliases
CreateConversationSerializer = CreateConversationRequest
SendMessageSerializer = SendMessageRequest
PatchConversationSerializer = PatchConversationRequest
