from rest_framework import serializers


class AddFavoriteRequest(serializers.Serializer):
    product_id = serializers.UUIDField()


# Backward-compatibility alias
AddFavoriteSerializer = AddFavoriteRequest
