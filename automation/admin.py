from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Device

admin.site.register(Room)
admin.site.register(Device)
