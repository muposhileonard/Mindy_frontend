from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=f"user{instance.id}",
            surname="Unknown",
            birthday="2000-01-01",
            gender="unspecified",
            education="Unknown",
            occupation="Mindy Explorer",
            bio="👋 I'm new to Mindy!",
            website="https://mindy.app"
        )
