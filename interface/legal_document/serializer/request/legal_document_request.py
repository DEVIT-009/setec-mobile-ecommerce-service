from rest_framework import serializers

LEGAL_DOC_TYPE_CHOICES = ['terms_of_service', 'privacy_policy', 'cookie_policy', 'refund_policy']


class AdminLegalDocumentCreateRequest(serializers.Serializer):
    type = serializers.ChoiceField(choices=LEGAL_DOC_TYPE_CHOICES)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    version = serializers.CharField(max_length=50, required=False)
    effective_date = serializers.DateField(required=False)


# Backward-compatibility alias
AdminLegalDocumentCreateSerializer = AdminLegalDocumentCreateRequest
