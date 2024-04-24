from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    """Custom manager for the custom user model."""

    def create_user(
        self, email: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """Create and return a regular user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user model.

        Returns:
            AbstractBaseUser: The newly created user.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """Create and return a superuser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the user model.

        Returns:
            AbstractBaseUser: The newly created superuser.

        Raises:
            ValueError: If is_staff or is_superuser fields are not set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
