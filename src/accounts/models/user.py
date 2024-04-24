from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model representing a user account.

    Attributes:
        email (str): The unique email address of the user.
        username (str): The unique username of the user.
        date_of_birth (Optional[date]): The date of birth of the user (optional).
        date_joined (datetime): The date and time when the user registered.
        is_active (bool): A flag indicating whether the user account is active.
        is_staff (bool): A flag indicating whether the user is a staff member.
        is_superuser (bool): A flag indicating whether the user has superuser privileges.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(
        verbose_name='registered',
        auto_now_add=True
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_username(self) -> str:
        """Return the username of the user."""
        username = f"{self.email}"
        return username.strip()

    def age(self) -> Optional[int]:
        """Calculate the age of the user based on the date of birth.

        Returns:
            Optional[int]: The age of the user, or None if the date of birth is not set.
        """

        if not self.date_of_birth:
            return None
        n, b = now().date(), self.date_of_birth
        return int(
            n.year
            - b.year
            - (
                0
                if n.month > b.month or n.month == b.month and n.day >= b.day
                else 1
            )
        )
