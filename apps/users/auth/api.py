# Third Party Stuff
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

# Talana Stuff
from apps.base import response
from apps.base.api.mixins import MultipleSerializerMixin
from apps.celery import app
from apps.users import services as user_services

from . import (  # services,
    serializers,
    tokens,
)


class AuthViewSet(MultipleSerializerMixin, viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    serializer_classes = {
        "login": serializers.LoginSerializer,
        "register": serializers.RegisterBasicSerializer,
        "logout": serializers.EmptySerializer,
        "password_change": serializers.PasswordChangeSerializer,
        "password_reset": serializers.PasswordResetSerializer,
        "password_reset_confirm": serializers.PasswordResetConfirmSerializer,
    }

    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_services.get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return response.Ok(data)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_services.create_user_account(**serializer.validated_data)

        app.send_task("apps.base.tasks.send_password_reset_mail", (user.id,))

        data = serializers.AuthUserSerializer(user).data
        return response.Created(data)

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """
        Calls Django logout method; Does not work for UserTokenAuth.
        """
        logout(request)
        return response.Ok({"success": _("Successfully logged out.")})

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return response.NoContent()

    @action(methods=["POST"], detail=False)
    def password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_services.get_user_by_email(serializer.data["email"])
        if user:
            app.send_task("apps.base.tasks.send_password_reset_mail", (user.id,))

        return response.Ok(
            {
                "message": _(
                    "Further instructions will be sent to the email if it exists"
                )
            }
        )

    @action(methods=["POST"], detail=False)
    def password_reset_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = tokens.get_user_for_password_reset_token(
            serializer.validated_data["token"]
        )
        user.set_password(serializer.validated_data["new_password"])
        user.is_verified = True
        user.save()
        return response.NoContent()
