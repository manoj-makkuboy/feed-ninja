from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging


class Category(models.Model):
    category_title = models.CharField(max_length=20, blank=False)
    category_summary = models.CharField(max_length=60, blank=True)


class CustomUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=40, blank=True)
    interested_categories = models.ForeignKey(Category)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customuser.save()


