from __future__ import annotations
import time
from typing import TYPE_CHECKING
from logging import getLogger

from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models.email_confirmation_code import EmailConfirmationCode

from core.business_logic.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError
)
from core.business_logic.services.confirm_email import send_confirm_code

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from core.business_logic.dto import RegistrationDTO


logger = getLogger(__name__)


def get_user_by_email(email: str) -> AbstractBaseUser | None:
    user_model = get_user_model()
    user = user_model.objects.filter(email=email).first()

    return user


def get_user_by_email_or_username(email_or_username: str) -> AbstractBaseUser | None:
    user_model = get_user_model()
    user = user_model.objects.filter(Q(email=email_or_username) | Q(username=email_or_username)).first()

    return user


def is_user_not_exists(email: str, username: str):
    user_model = get_user_model()
    if user_model.objects.filter(email=email, is_active=True).exists():
        logger.error('Email already exists', extra={'email': email})
        raise EmailAlreadyExistsError
    if user_model.objects.filter(username=username, is_active=True).exists():
        logger.error(
            'Username already exists', extra={'username': username}
        )
        raise UsernameAlreadyExistsError
    
    return True


def create_user(data: RegistrationDTO) -> AbstractBaseUser | None:
    logger.info('Get user creation request', extra={'user': data})

    user_model: AbstractBaseUser = get_user_model()
    
    email = data.email.lower()
    username = data.username.lower()

    user_not_exists = is_user_not_exists(email=email, username=username)

    if user_not_exists:

        existed_user = user_model.objects.filter(email=email).first()
        if existed_user:
            confirmation_code = EmailConfirmationCode.objects.filter(user=existed_user).first()
            if confirmation_code and time.time() <= confirmation_code.expiration:
                time_to_expire = confirmation_code.expiration - time.time()
                return {'result': False, 'time_to_expire': time_to_expire}

        user_model.objects.filter((Q(email=email) | Q(username=username)) & Q(is_active=False)).delete()

        created_user = user_model.objects.create_user(
            email=email,
            password=data.password,
            username=username,
            date_of_birth=data.date_of_birth,
        )

        logger.info('Register user', extra={'user_id': created_user.pk})
        is_send_code = send_confirm_code(user=created_user, email=email)

        return is_send_code
