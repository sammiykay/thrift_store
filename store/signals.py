from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DeliveryDriver

@receiver(post_save, sender=User)
def create_delivery_driver(sender, instance, created, **kwargs):
    # Create a delivery driver profile when a new user is created
    if created:
        DeliveryDriver.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_delivery_driver(sender, instance, **kwargs):
    # Save the delivery driver profile whenever the user is saved
    if hasattr(instance, 'delivery_driver'):
        instance.delivery_driver.save()
