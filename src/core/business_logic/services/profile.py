from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from django.db.models import Prefetch
from django.db import transaction

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

from accounts.models import Freelancer, Client, SocialLink
from core.business_logic.dto import ProfileEditDTO
from core.business_logic.services.common import (
    replace_file_name_to_uuid,
    change_file_size
)

logger = getLogger(__name__)

def get_freelancer_profile(user_id: int) -> Freelancer:
    social_links_prefetch = Prefetch(
        'social_links',
        queryset=SocialLink.objects.select_related('platform')
    )
    profile = Freelancer.objects.select_related('user').prefetch_related(social_links_prefetch).filter(user__pk=user_id).first()

    return profile


def get_client_profile(user_id: int) -> Freelancer:
    social_links_prefetch = Prefetch(
        'social_links',
        queryset=SocialLink.objects.select_related('platform')
    )
    profile = Client.objects.select_related('user').prefetch_related(social_links_prefetch).filter(user__pk=user_id).first()

    return profile


def initial_profile_form(user_id: int, profile_type: str = 'freelancer') -> dict[str, str]:
    """
    Function to populate a form with existing user data when editing user information.
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
    }

    return initial_data


def profile_edit(data: ProfileEditDTO, user: AbstractBaseUser, profile_type: str = 'freelancer') -> bool:

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

        profile.save()
        logger.info('Profile edited', extra={'data': logger_data})


# def delete_profile_avatar(user: AbstractBaseUser) -> None:
#     profile = Profile.objects.get(user=user)

#     profile.avatar = None
#     profile.save()
