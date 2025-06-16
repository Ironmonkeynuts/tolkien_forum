from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # If new user, create profile
        Profile.objects.create(user=instance)
    else:
        # If user exists, ensure profile exists
        Profile.objects.get_or_create(user=instance)