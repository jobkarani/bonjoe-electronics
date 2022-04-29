from .models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
