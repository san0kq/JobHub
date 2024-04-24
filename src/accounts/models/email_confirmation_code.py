from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class EmailConfirmationCode(BaseModel):
    """Represents an email confirmation code associated with a user.

    Attributes:
        code (str): The unique confirmation code.
        user (User): The user associated with the confirmation code.
        expiration (int): The expiration time of the confirmation code (in seconds).
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
        """Returns a string representation of the email confirmation code.

        Returns:
            str: The string representation of the confirmation code.
        """

        return f"{self.code}"
