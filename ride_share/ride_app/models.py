from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seats_available = models.IntegerField()
    start_date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return f"{self.driver.first_name} {self.driver.last_name} | {self.origin} to {self.destination}: {self.status}"