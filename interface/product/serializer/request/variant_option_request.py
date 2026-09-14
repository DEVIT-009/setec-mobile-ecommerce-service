from rest_framework import serializers


class VariantOptionRequest(serializers.Serializer):
    variant_id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=100)


class VariantOptionPartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    value = serializers.CharField(max_length=100, required=False)
