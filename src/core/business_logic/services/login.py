from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.contrib.auth import authenticate

if TYPE_CHECKING:
    from core.business_logic.dto import LoginDTO
    from django.contrib.auth.models import AbstractBaseUser

from core.business_logic.exceptions import InvalidAuthCredentials

logger = getLogger(__name__)


def authenticate_user(data: LoginDTO) -> dict[str, AbstractBaseUser | None] | None:
    """
    User authentication on the website.
    """
    user = authenticate(username=data.email_or_username.lower(), password=data.password)
    if user:
        logger.info("Successfully login", extra={"login_data": data.email_or_username.lower()})
        return user
    else:
        logger.error("Invalid credentials", extra={"login_data": data.email_or_username.lower()})
        raise InvalidAuthCredentials("Invalid credentials.")
