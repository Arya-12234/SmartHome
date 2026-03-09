from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AutomationRule

@receiver(post_save, sender=AutomationRule)
def process_automation_rule(sender, instance, **kwargs):
    if instance.trigger_event == "motion_detected":
        print(f"Executing: {instance.action} on device {instance.device_id}")
