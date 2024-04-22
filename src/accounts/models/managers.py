from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    """
    A custom manager is used to create
    regular users and superusers.

    It's utilized for the functionality of a custom user model.
    """

    def create_user(
        self, email: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """Creates and saves a User with the given data."""
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user: AbstractBaseUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """Creates and saves a superuser with the given data."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
