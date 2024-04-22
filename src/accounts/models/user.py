from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    Registration is done through email.
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
        username = f"{self.email}"
        return username.strip()

    def age(self) -> Optional[int]:
        """
        Calculate the age of the user.
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
