from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta, timezone

class RideShareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    student_id = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return datetime.now(timezone.utc) - self.created_at < timedelta(days=1)

    def __str__(self):
        return f"Token for {self.user.username}"
    
