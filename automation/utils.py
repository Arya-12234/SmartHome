import geopy.distance

HOME_LOCATION = (37.7749, -122.4194)  # Replace with actual home coordinates

def is_user_near_home(user_location):
    distance = geopy.distance.distance(HOME_LOCATION, (user_location.latitude, user_location.longitude)).km
    return distance < 0.5  # Within 500 meters

def check_and_trigger_geofencing(user):
    from .models import UserLocation
    location = UserLocation.objects.get(user=user)
    if is_user_near_home(location):
        print(f"User {user.username} is near home. Turning on AC.")
