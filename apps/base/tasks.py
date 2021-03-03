# Standard Library
import functools
import logging

# Third Party Stuff
from celery.exceptions import SoftTimeLimitExceeded
from django.conf import settings
from mail_templated import send_mail

# Talana Stuff
from apps.celery import app
from apps.users.auth.tokens import get_token_for_password_reset
from apps.users.models import User

logger = logging.getLogger(__name__)


def soft_time_limit_handler(
    ignore_result=False, soft_time_limit=15, max_retries=3, countdown=60
):
    """
    Decorator to wrap celery tasks in try-except clause, which will kill and then
    re-queue the task if it does not complete within the soft_time_limit.
    Decorated task will be re-queued after a cooldown period determined by countdown param.
    Defaults 15 second time limit, 60 second period before retrying, and 1 retry.

    :param soft_time_limit int
    :param max_retries int
    :param countdown int
    """

    def decorator(func):
        @app.task(
            ignore_result=ignore_result,
            bind=True,
            soft_time_limit=soft_time_limit,
            max_retries=max_retries,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SoftTimeLimitExceeded as exception:
                wrapper.retry(exc=exception, countdown=countdown)

        return wrapper

    return decorator


@soft_time_limit_handler(ignore_result=True, soft_time_limit=5)
def send_password_reset_mail(
    self, user_id, template_name="email/password_reset_mail.tpl"
):
    user = User.objects.get(id=user_id)
    ctx = {"user": user, "token": get_token_for_password_reset(user)}

    return send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        template_name=template_name,
        context=ctx,
    )
