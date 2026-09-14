from rest_framework import serializers


class CreateReviewRequest(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    title = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)
    order_item_id = serializers.UUIDField(required=False, allow_null=True)


class UpdateReviewRequest(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    title = serializers.CharField(required=False, allow_blank=True)
    body = serializers.CharField(required=False, allow_blank=True)


class AdminUpdateReviewStatusRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=['pending', 'published', 'rejected', 'archived'])


# Backward-compatibility aliases
CreateReviewSerializer = CreateReviewRequest
UpdateReviewSerializer = UpdateReviewRequest
