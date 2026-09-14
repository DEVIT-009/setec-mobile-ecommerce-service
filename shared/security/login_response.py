from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    accessToken = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField()
    data = TokenSerializer()