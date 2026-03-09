from celery import shared_task
from datetime import datetime

@shared_task
def turn_on_lights():
    # Send a signal to IoT device to turn on lights
    print(f"Lights turned on at {datetime.now()}")
