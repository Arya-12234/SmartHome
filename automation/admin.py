from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



from .models import Device, UserPreferences, PricingPlan, Payment

admin.site.register(Device)
from .models import ChatHistory

admin.site.register(ChatHistory)

admin.site.register(PricingPlan)
admin.site.register(Payment)


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'lighting_day', 'lighting_night', 'security_alarm', 'security_curtains']


