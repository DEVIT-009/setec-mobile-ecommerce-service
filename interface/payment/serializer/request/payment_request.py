from rest_framework import serializers


class CompleteInternalPaymentRequest(serializers.Serializer):
    idempotency_key = serializers.CharField(max_length=128)
    simulate_outcome = serializers.ChoiceField(
        choices=['succeeded', 'failed'],
        default='succeeded',
    )
    failure_reason = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class CompleteInternalPaymentBatchRequest(serializers.Serializer):
    idempotency_key = serializers.CharField(max_length=128)
    order_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        max_length=100,
    )
    simulate_outcome = serializers.ChoiceField(
        choices=['succeeded', 'failed'],
        default='succeeded',
    )
    failure_reason = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    def validate_order_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Order IDs must be unique.")
        return value
