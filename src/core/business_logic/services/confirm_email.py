from __future__ import annotations

import time
import uuid
from logging import getLogger
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.template import loader

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

from accounts.models import EmailConfirmationCode
from core.business_logic.exceptions import (
    ConfirmationCodeExpired,
    ConfirmationCodeNotExists,
)

logger = getLogger(__name__)

def send_confirm_code(user: AbstractBaseUser, email: str) -> None:
    """
    Generates and sends a confirmation code for registration or email change to the user's email.
    """
    new_confirmation_code = str(uuid.uuid4())
    code_expiration_time = (
        int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME
    )

    confirmation_code = EmailConfirmationCode.objects.filter(user=user).first()

    if not confirmation_code or (confirmation_code and time.time() > confirmation_code.expiration):
        if confirmation_code:
            confirmation_code.delete()
        EmailConfirmationCode.objects.create(
            code=new_confirmation_code, user=user, expiration=code_expiration_time
        )

        confirm_url = (
            settings.EMAIL_REVERSE_URL
            + reverse('accounts:register_confirm')
            + f'?code={new_confirmation_code}'
            + f'&email={email}'
        )
        print(confirm_url)

        template = loader.render_to_string('email/register.txt', {
            'username': user.username,
            'confirmation_url': confirm_url
        })

        send_mail(
            subject='no-reply',
            message='',
            html_message=template,
            from_email=settings.EMAIL_FROM,
            recipient_list=[email],
        )
        logger.info(
            'Send confirmation code',
            extra={'code': new_confirmation_code, 'email': email},
        )
        return {'result': True}
    else:
        time_to_expire = confirmation_code.expiration - time.time()
        logger.info(
            "The code has not been sent. The previous code's lifespan has not yet expired.",
            extra={'email': email, 'time_to_expire': time_to_expire}
        )
        return {'result': False, 'time_to_expire': time_to_expire}


def confirm_user_email(confirmation_code: str, email: str) -> AbstractBaseUser:
    """
    Used to access the database to authenticate the code received by the user via email.
    """
    try:
        code_data = EmailConfirmationCode.objects.get(code=confirmation_code)
    except EmailConfirmationCode.DoesNotExist as err:
        logger.error(
            "Provided code doesn't exists.",
            exc_info=err,
            extra={'code': confirmation_code},
        )
        raise ConfirmationCodeNotExists

    if time.time() > code_data.expiration:
        logger.info(
            'Provided expiration code expired.',
            extra={
                'current_time': str(time.time()),
                'code_expiration': str(code_data.expiration),
            },
        )
        raise ConfirmationCodeExpired

    user = code_data.user
    user.is_active = True
    user.save()
    logger.info('User is active', extra={'user': user.username})

    code_data.delete()

    return user
