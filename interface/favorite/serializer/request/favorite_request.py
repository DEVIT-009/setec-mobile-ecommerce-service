from rest_framework import serializers


class AddFavoriteRequest(serializers.Serializer):
    product_id = serializers.CharField()


# Backward-compatibility alias
AddFavoriteSerializer = AddFavoriteRequest
