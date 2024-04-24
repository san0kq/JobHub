from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import os

from accounts.models import Client, Freelancer


@receiver(pre_save, sender=Client)
@receiver(pre_save, sender=Freelancer)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.avatar != instance.avatar:
            delete_avatar(old_instance)
        elif not instance.avatar:
            delete_avatar(old_instance)

def delete_avatar(user_profile):
    if user_profile.avatar:
        avatar_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.avatar))
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
