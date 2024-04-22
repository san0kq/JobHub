from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel


class Client(BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='client',
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Freelancer(BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='freelancer',
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'freelancer'
        verbose_name_plural = 'freelancers'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
