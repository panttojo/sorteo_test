# Third Party Stuff
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# Talana Stuff
from apps.users import services as user_services
from apps.users.models import UserManager
from apps.users.serializers import UserSerializer

from . import tokens


class EmptySerializer(serializers.Serializer):
    pass


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class RegisterBasicSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=120)
    last_name = serializers.CharField(required=True, max_length=120)
    password = serializers.CharField(required=False)

    def validate_password(self, value):
        if value is not None:
            password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        user = user_services.get_user_by_email(email=value)
        if user:
            raise serializers.ValidationError(_("Email is already taken."))
        return UserManager.normalize_email(value)


class AuthUserSerializer(UserSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["auth_token"]

    def get_auth_token(self, obj):
        return tokens.get_token_for_user(obj, "authentication")


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    default_error_messages = {"invalid_password": _("Current password does not match")}

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(
                self.default_error_messages["invalid_password"]
            )
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
