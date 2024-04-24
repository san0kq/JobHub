from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel


class ProfileBase(BaseModel):
    """Base model for user profiles containing common fields.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        avatar (str): The path to the user's avatar image.
        phone (str): The phone number of the user.
        email (str): The email address of the user.
        telegram_link (str): The Telegram profile link of the user.
        linkedin_link (str): The LinkedIn profile link of the user.
    """

    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telegram_link = models.URLField(max_length=200, null=True, blank=True)
    linkedin_link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class Client(ProfileBase):
    """Model representing a client user with additional profile information.

    Attributes:
        user (User): The associated user instance.
    """

    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='client',
    )

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self) -> str:
        """Return a string representation of the client."""
        return f'{self.first_name} {self.last_name}'


class Freelancer(ProfileBase):
    """Model representing a freelancer user with additional profile information.

    Attributes:
        user (User): The associated user instance.
    """

    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='freelancer',
    )

    class Meta:
        verbose_name = 'freelancer'
        verbose_name_plural = 'freelancers'

    def __str__(self) -> str:
        """Return a string representation of the freelancer."""
        return f'{self.first_name} {self.last_name}'
