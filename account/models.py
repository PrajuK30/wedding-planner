from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=[
        ('Wedding Family', 'Wedding Family'),
        ('Food Caterer', 'Food Caterer'),
        ('Decorator', 'Decorator'),
        ('Event Planner', 'Event Planner'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    mobile = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    age = models.PositiveIntegerField(null=True, blank=True)  # ✅ NEW FIELD

    is_verified = models.BooleanField(default=False)  # ✅ Optional for OTP verification

    def __str__(self):
        return self.username
