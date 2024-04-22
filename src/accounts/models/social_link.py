from django.db import models

from core.models import BaseModel


class SocialPlatform(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'social platform'
        verbose_name_plural = 'social platforms'

    def __str__(self) -> str:
        return f'{self.name}'


class SocialLink(BaseModel):
    platform = models.ForeignKey(
        to=SocialPlatform,
        on_delete=models.CASCADE,
        related_name='social_links',
        related_query_name='social_link'
    )
    url = models.URLField(
        max_length=200,
    )
    client = models.ForeignKey(
        to='Client',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='social_links',
        related_query_name='social_link',
    )
    freelancer = models.ForeignKey(
        to='Freelancer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='social_links',
        related_query_name='social_link',
    )

    class Meta:
        verbose_name = 'social link'
        verbose_name_plural = 'social links'

    def __str__(self) -> str:
        return self.pk
