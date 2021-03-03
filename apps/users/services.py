# Third Party Stuff
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.utils.translation import gettext_lazy as _

# Talana Stuff
from apps.base import exceptions as exc


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise exc.WrongArguments(_("Invalid username/password. Please try again!"))

    return user


def create_user_account(email, first_name="", last_name="", password=None):
    user = get_user_model().objects.create_user(
        email=email, first_name=first_name, last_name=last_name, password=password
    )
    return user


def get_user_by_email(email: str):
    return get_user_model().objects.filter(email__iexact=email).first()
