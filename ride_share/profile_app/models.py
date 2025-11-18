from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from supabase import create_client, Client
import uuid

def user_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"profile_photos/user_{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # If full_name is not set, use the user's first and last name
        if not self.full_name and (self.user.first_name or self.user.last_name):
            self.full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
