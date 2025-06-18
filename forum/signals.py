from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Listens for the post-save signal from User model
# When a user model is created or updated the function runs automatically

# Connects function create_or_update_profile to run after any User is saved
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that ensures every User has a linked Profile.
    Runs after a User is saved (created or updated).

    - If created → create a new Profile.
    - If updated → ensure Profile exists, or create if missing.
    """
    profile, profile_created = Profile.objects.get_or_create(user=instance)

    if created:
        # New user, profile just created — you can set defaults if needed
        profile.user_type = 'member'  # Example default user type
        profile.save()
