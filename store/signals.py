from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Purchase

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Purchase)
def update_loyalty_points(sender, instance, created, **kwargs):
    if created:  # Only update loyalty points if it's a new purchase
        try:
            user_profile = instance.user.userprofile  # Access the user profile correctly
            user_profile.loyalty_points += instance.loyalty_points  # Add loyalty points
            user_profile.save()  # Save the updated profile
        except UserProfile.DoesNotExist:
            print(f"UserProfile for user {instance.user.username} not found.")