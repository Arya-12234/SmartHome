

# Create your models here.
import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Device model for managing smart home devices
class Device(models.Model):
    DEVICE_TYPES = [
        ('light', 'Light'),
        ('heater', 'Heater'),
        ('security', 'Security'),
    ]

    # Foreign key linking the device to a user (optional, allows nulls)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Device attributes
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100, choices=DEVICE_TYPES)
    status = models.BooleanField(default=False)

    # Optional fields for specific devices
    brightness = models.IntegerField(null=True, blank=True)  # For light devices
    temperature = models.IntegerField(null=True, blank=True)  # For heater devices

    # Usage and timing data
    last_used = models.DateTimeField(null=True, blank=True)
    total_usage_time = models.DurationField(default=timedelta())

    def __str__(self):
        return self.name

# ChatHistory model for managing chatbot interactions
class ChatHistory(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('system', 'System'),
        ('error', 'Error'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('pending', 'Pending'),
        ('executed', 'Executed'),
        ('not_supported', 'Not Supported'),
        ('validation_failed', 'Validation Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the Django User model
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='user')
    user_message = models.TextField()
    bot_response = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True)  # Linked to Device model
    command = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_details = models.TextField(null=True, blank=True)  # For storing error logs or details
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),  # Index for faster filtering by timestamp
        ]
        verbose_name_plural = "Chat Histories"  # Better plural form in admin panel

    def __str__(self):
        return (f"Session {self.session_id} | {self.user_message} -> {self.bot_response} | "
                f"Status: {self.status} | Device: {self.device.name if self.device else 'N/A'}")



class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lighting_day = models.CharField(max_length=10, choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright')
    lighting_night = models.CharField(max_length=10, choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright')
    security_alarm = models.CharField(max_length=10, choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled')
    security_curtains = models.CharField(max_length=10, choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto')
    security_gate = models.CharField(max_length=10, choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto')
    heating_shower = models.CharField(max_length=10, choices=[('on', 'On'), ('off', 'Off')], default='off')


    def __str__(self):
        return f"Preferences for {self.user.username}"





class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



from django.db import models

class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Add this line if it's missing
    icon = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=255)
    unavailable = models.BooleanField(default=False)
    plan = models.ForeignKey(PricingPlan, related_name='features', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


from django.db import models

class Payment(models.Model):
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)  # Update this to reference PricingPlan

    def __str__(self):
        return self.transaction_id

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)  # Changed to EmailField

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='automation_user_set',  # Custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='automation_user_permissions_set',  # Custom related name
        blank=True
    )




