from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seats_available = models.IntegerField(default=1)
    start_date = models.DateField()
    start_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # default 0
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return f"{self.driver.first_name} {self.driver.last_name} | {self.origin} to {self.destination}: {self.status}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    num_seats = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.first_name} booked {self.num_seats} seats on {self.ride}"