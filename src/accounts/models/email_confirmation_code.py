from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class EmailConfirmationCode(BaseModel):
    """
    It's used for storing confirmation codes
    sent to email during registration or email change.
    It's tied to the user and has
    a specified storage time in Unix format.
    """

    code = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='email_confirmation_codes',
        related_query_name='email_confirmation_code',
    )
    expiration = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'email_confirmation_codes'

    def __str__(self) -> str:
        return f"{self.code}"
