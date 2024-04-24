from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from django.db import transaction

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from core.business_logic.dto import ProfileEditDTO

from accounts.models import Freelancer, Client
from core.business_logic.services.common import (
    replace_file_name_to_uuid,
    change_file_size
)

logger = getLogger(__name__)

def get_freelancer_profile(user_id: int) -> Freelancer:
    """
    Retrieve the freelancer profile for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Freelancer: The freelancer profile of the user.
    """
    profile = Freelancer.objects.select_related('user').filter(user__pk=user_id).first()

    return profile


def get_client_profile(user_id: int) -> Freelancer:
    """
    Retrieve the client profile for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Client: The client profile of the user.
    """
    profile = Client.objects.select_related('user').filter(user__pk=user_id).first()

    return profile


def initial_profile_form(user_id: int, profile_type: str = 'freelancer') -> dict[str, str]:
    """
    Get initial profile data for the profile edit form.

    Args:
        user_id (int): The ID of the user.
        profile_type (str): The type of profile ('freelancer' or 'client'). Defaults to 'freelancer'.

    Returns:
        dict: Initial data for the profile edit form.
    """
    if profile_type == 'freelancer':
        profile = get_freelancer_profile(user_id=user_id)
    else:
        profile = get_client_profile(user_id=user_id)

    initial_data = {
        'first_name': profile.first_name if profile else '',
        'last_name': profile.last_name if profile else '',
        'phone': profile.phone if profile else '',
        'email': profile.email if profile else '',
        'avatar': profile.avatar if profile else '',
        'linkedin': profile.linkedin_link if profile else '',
        'telegram': profile.telegram_link if profile else ''
    }

    return initial_data


def profile_edit(
        data: ProfileEditDTO,
        user: AbstractBaseUser,
        profile_type: str = 'freelancer'
    ) -> bool:
    """
    Edit the user's profile.

    Args:
        data (ProfileEditDTO): The profile data to edit.
        user (AbstractBaseUser): The user object.
        profile_type (str): The type of profile ('freelancer' or 'client'). Defaults to 'freelancer'.

    Returns:
        None
    """
    with transaction.atomic():
        if profile_type == 'freelancer':
            profile = Freelancer.objects.get_or_create(user=user)[0]
        else:
            profile = Client.objects.get_or_create(user=user)[0]
        logger_data = {}
        
        if profile.email and profile.email.lower() != data.email.lower():
            logger_data['old_email'] = profile.email
            logger_data['new_email'] = data.email.lower()
            profile.email = data.email.lower()
        elif not profile.email and data.email:
            logger_data['new_email'] = data.email.lower()
            profile.email = data.email.lower()

        if profile.first_name != data.first_name:
            if profile.first_name:
                logger_data['old_first_name'] = profile.first_name
            logger_data['new_first_name'] = data.first_name
            profile.first_name = data.first_name

        if profile.last_name != data.last_name:
            if profile.last_name:
                logger_data['old_last_name'] = profile.last_name
            logger_data['new_last_name'] = data.last_name
            profile.last_name = data.last_name
        
        if profile.phone != data.phone:
            if profile.phone:
                logger_data['old_phone'] = profile.phone
            logger_data['new_phone'] = data.phone
            profile.phone = data.phone

        if profile.avatar != data.avatar:
            if data.avatar:
                data.avatar = replace_file_name_to_uuid(file=data.avatar)
                data.avatar = change_file_size(file=data.avatar)
                profile.avatar = data.avatar
            elif data.avatar is False:
                profile.avatar = None
        
        if profile.telegram_link != data.telegram:
            if profile.telegram_link:
                logger_data['old_telegram'] = profile.telegram_link
            logger_data['new_telegram'] = data.telegram
            profile.telegram_link = data.telegram
        
        if profile.linkedin_link != data.linkedin:
            if profile.linkedin_link:
                logger_data['old_linkedin'] = profile.linkedin_link
            logger_data['new_linkedin'] = data.linkedin
            profile.linkedin_link = data.linkedin

        profile.save()
        logger.info('Profile edited', extra={'data': logger_data})


def delete_profile_avatar(user: AbstractBaseUser, profile_type: str = 'freelancer') -> None:
    """
    Delete the avatar of the user's profile.

    Args:
        user (AbstractBaseUser): The user object.
        profile_type (str): The type of profile ('freelancer' or 'client'). Defaults to 'freelancer'.

    Returns:
        None
    """
    if profile_type == 'client':
        profile = Client.objects.get(user=user)
    else:
        profile = Freelancer.objects.get(user=user)

    profile.avatar = None
    profile.save()
