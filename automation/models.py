from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role='family_member'):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('family_member', 'Family Member'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='family_member')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return self.name


class Device(models.Model):
    DEVICE_TYPES = (
        ("light_bulb", "Light Bulb"),
        ("smart_gate", "Smart Gate System"),
        ("shower_heating", "Shower Heating"),
    )

    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    status = models.BooleanField(default=False)  # True = ON, False = OFF
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="devices")

    def __str__(self):
        return f"{self.name} ({'ON' if self.status else 'OFF'})"


class AutomationRule(models.Model):
    TRIGGER_CHOICES = [
        ('motion_detected', 'Motion Detected'),
        ('temperature_high', 'High Temperature'),
        ('door_open', 'Door Open'),
    ]

    ACTION_CHOICES = [
        ('turn_on_lights', 'Turn On Lights'),
        ('turn_on_ac', 'Turn On AC'),
    ]

    trigger_event = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="automation_rules")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"If {self.trigger_event}, then {self.action}"


class UserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"

class UserPreferences(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    lighting_day = models.CharField(max_length=10, choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright')
    lighting_night = models.CharField(max_length=10, choices=[('dim', 'Dim'), ('bright', 'Bright')], default='bright')
    security_alarm = models.CharField(max_length=10, choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled')
    security_curtains = models.CharField(max_length=10, choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto')
    security_gate = models.CharField(max_length=10, choices=[('auto', 'Automatic'), ('manual', 'Manual')], default='auto')
    heating_shower = models.CharField(max_length=10, choices=[('on', 'On'), ('off', 'Off')], default='off')


    def __str__(self):
        return f"Preferences for {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    MyUser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[("light", "Light"), ("dark", "Dark")], default="light")
    notifications = models.BooleanField(default=True)
    energy_saving = models.BooleanField(default=False)
    security_mode = models.BooleanField(default=False)
    temp_alerts = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings for {self.user.username}"

from django.conf import settings
class ChatbotQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.query[:50]}"
    



from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True)

    def __str__(self):
        return self.name
