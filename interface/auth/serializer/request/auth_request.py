from rest_framework import serializers


class RegisterRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)


class LoginRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ForgotPasswordRequest(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordRequest(serializers.Serializer):
    reset_token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class VerifyPhoneRequest(serializers.Serializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)


# Backward-compatibility aliases
RegisterSerializer = RegisterRequest
LoginSerializer = LoginRequest
ForgotPasswordSerializer = ForgotPasswordRequest
ResetPasswordSerializer = ResetPasswordRequest
VerifyPhoneSerializer = VerifyPhoneRequest
