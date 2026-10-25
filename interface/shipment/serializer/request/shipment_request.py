from rest_framework import serializers


class CreateShipmentRequest(serializers.Serializer):
    note = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class PackShipmentRequest(serializers.Serializer):
    note = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class HandoffShipmentRequest(serializers.Serializer):
    carrier_name = serializers.CharField(max_length=100)
    tracking_number = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    note = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class UpdateShipmentTrackingRequest(serializers.Serializer):
    carrier_name = serializers.CharField(max_length=100, required=False)
    tracking_number = serializers.CharField(max_length=100, required=False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide carrier_name or tracking_number.")
        return attrs


class ShipmentCheckpointRequest(serializers.Serializer):
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    description = serializers.CharField(max_length=1000)
    event_time = serializers.DateTimeField(required=False)


class OutForDeliveryRequest(serializers.Serializer):
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    note = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class ConfirmDeliveryRequest(serializers.Serializer):
    note = serializers.CharField(max_length=1000, required=False, allow_blank=True)
