from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank user
    user_wallet = models.CharField(max_length=255, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    loyalty_points = models.IntegerField(default=10)

    def __str__(self):
        return f"Purchase of {self.product.name} by {self.user.username if self.user else 'Unknown User'}"

    def save(self, *args, **kwargs):
        if not self.user:  # If no user is assigned
            pass
        super().save(*args, **kwargs)

        # Optionally update loyalty points if user exists (after saving)
        if self.user:
            user_profile, created = UserProfile.objects.get_or_create(user=self.user)
            user_profile.loyalty_points += self.loyalty_points
            user_profile.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()