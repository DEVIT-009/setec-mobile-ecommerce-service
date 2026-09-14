from rest_framework import serializers


class UserUpdateRequest(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False)


class ProfileUpdateRequest(serializers.Serializer):
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other', 'prefer_not_to_say'], required=False)
    preferred_language = serializers.CharField(required=False, max_length=10)
    marketing_opt_in = serializers.BooleanField(required=False)


class SecurityUpdateRequest(serializers.Serializer):
    two_factor_enabled = serializers.BooleanField(required=False)
    biometric_enabled = serializers.BooleanField(required=False)


# Backward-compatibility aliases
UserUpdateSerializer = UserUpdateRequest
ProfileUpdateSerializer = ProfileUpdateRequest
SecurityUpdateSerializer = SecurityUpdateRequest
