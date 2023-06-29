from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer


# This is a signal receiver function that gets called after a User instance is saved
# If a new User instance is created (not updated), it automatically creates a corresponding Customer instance
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
