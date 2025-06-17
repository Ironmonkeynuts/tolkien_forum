from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Listens for the post-save signal from User model
# When a user model is created or updated the function runs automatically

# Connects function create_or_update_profile to run after any User is saved
@receiver(post_save, sender=User)
# Checks instance of user is already created
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # If new user, create profile
        Profile.objects.create(user=instance)
    else:
        # If user exists, ensure profile exists
        Profile.objects.get_or_create(user=instance)
    # Save profile in all cases (trigger signals or update timestamp)
    instance.profile.save()

