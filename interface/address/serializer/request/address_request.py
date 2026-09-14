from rest_framework import serializers


class AddressRequest(serializers.Serializer):
    label = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    recipient_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=32)
    address_line_1 = serializers.CharField(max_length=255)
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=255)
    city = serializers.CharField(max_length=120)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=120)
    postal_code = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=32)
    country_code = serializers.CharField(max_length=2)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False, allow_null=True)
    is_default = serializers.BooleanField(required=False, default=False)


class AddressPartialRequest(serializers.Serializer):
    label = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    recipient_name = serializers.CharField(required=False, max_length=255)
    phone_number = serializers.CharField(required=False, max_length=32)
    address_line_1 = serializers.CharField(required=False, max_length=255)
    address_line_2 = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=255)
    city = serializers.CharField(required=False, max_length=120)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=120)
    postal_code = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=32)
    country_code = serializers.CharField(required=False, max_length=2)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False, allow_null=True)
    is_default = serializers.BooleanField(required=False)


# Backward-compatibility alias
AddressSerializer = AddressRequest
