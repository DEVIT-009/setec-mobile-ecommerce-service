from rest_framework import serializers


class CloudinarySignatureRequest(serializers.Serializer):
    folder = serializers.CharField(required=False, default="uploads")


class ConfirmUploadRequest(serializers.Serializer):
    public_id = serializers.CharField()
    url = serializers.URLField()
    secure_url = serializers.URLField(required=False)
    mime_type = serializers.CharField(required=False, allow_blank=True)
    usage_type = serializers.CharField(required=False, allow_blank=True)


# Backward-compatibility aliases
CloudinarySignatureSerializer = CloudinarySignatureRequest
ConfirmUploadSerializer = ConfirmUploadRequest
