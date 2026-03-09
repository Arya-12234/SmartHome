import base64
from datetime import datetime
from pyexpat.errors import messages
import time
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RoomSerializer, UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .models import MyUser, UserPreferences
from django.contrib.auth.decorators import login_required
import requests

class UserRegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

from rest_framework import generics, permissions
from .models import Room
from rest_framework_simplejwt.authentication import JWTAuthentication



class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class RoomRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def room_view(request):
    rooms = Room.objects.all()
    user_name = request.user.username
    context = {
        'rooms': rooms,
        'user_name': user_name
    }
    return render(request, 'room.html', context)




from .models import Device
from .serializers import DeviceSerializer
from rest_framework.exceptions import PermissionDenied

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room = serializer.validated_data.get("room")
        if room.user != self.request.user:
            raise PermissionDenied("You can only add devices to your own rooms.")
        serializer.save()

class DeviceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]



from .models import Device

def devices_view(request):
    devices = Device.objects.all()  # Use the correct model name
    return render(request, 'devices.html', {'devices': devices})



from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import AutomationRule
from .serializers import AutomationRuleSerializer

class AutomationRuleView(generics.ListCreateAPIView):
    queryset = AutomationRule.objects.all()
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


@login_required
def update_preferences(request):
    # Get the user's preferences or create new ones if they don't exist
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update preferences with the form data
        preferences.theme = request.POST.get('theme', 'light')
        preferences.notifications_enabled = 'notifications_enabled' in request.POST
        preferences.save()
        return redirect('dashboard')  # Redirect to the same page after saving

    # Render the preferences page with the current preferences
    return render(request, 'preferences.html', {'preferences': preferences})


# Home View
def home(request):
    plans=Plan.objects.all()

    if request.user.is_authenticated:
        user = request.user  # You can now pass the user object directly to the template
    else:
        user = None
    return render(request, 'home.html', {'user': user, 'plans':plans})


# Dashboard View
@login_required(login_url='login')
def dashboard(request):
    # Get all devices for the user
    devices = Device.objects.filter(user=request.user)

    total_devices = devices.count()
    active_devices = devices.filter(status=True).count()
    total_usage_time = devices.aggregate(total_time=Sum('total_usage_time'))['total_time'] or 0

    # Example of chart data (can be modified to suit your needs)
    devices_data = {
        'labels': ['Active', 'Inactive'],
        'data': [active_devices, total_devices - active_devices],
    }

    context = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'total_usage_time': total_usage_time,
        'devices_data': devices_data,
        'devices': devices,  # Pass the devices list to the template
    }

    return render(request, 'accounts/dashboard.html', context)


# About View
def about(request):
    return render(request, 'about.html')

# Services View
def services(request):
    return render(request, 'services.html')


# Contact View
def contact(request):
    if request.method == 'POST':
        # Handle form submission logic here (save to DB, send email, etc.)
        # Redirect or show a success message
        pass
    return render(request, 'contact.html')

from .forms import UserPreferencesForm
# Profile View
@login_required(login_url='login')
def profile_view(request):
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(request, 'accounts/profile.html', {'form': form})

# User Preferences View
@login_required(login_url='login')
def preferences(request):
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        notifications_enabled = 'notifications_enabled' in request.POST

        preferences.theme = theme
        preferences.notifications_enabled = notifications_enabled
        preferences.save()

        # Show success message and redirect to dashboard
        messages.success(request, 'Preferences updated successfully!')
        return redirect('dashboard')

    return render(request, 'preferences.html', {'preferences': preferences})

@login_required
def update_preferences(request):
    # Get the user's preferences or create new ones if they don't exist
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update preferences with the form data
        preferences.theme = request.POST.get('theme', 'light')
        preferences.notifications_enabled = 'notifications_enabled' in request.POST
        preferences.save()
        return redirect('dashboard')  # Redirect to the same page after saving

    # Render the preferences page with the current preferences
    return render(request, 'preferences.html', {'preferences': preferences})


# Set Device Brightness
@login_required(login_url='login')
def set_brightness(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    if request.method == "POST":
        brightness = request.POST.get('brightness')
        try:
            device.brightness = int(brightness)
            device.save()
            messages.success(request, f"Brightness for '{device.name}' set to {brightness}")
        except ValueError:
            messages.error(request, 'Invalid brightness value')
    return redirect('dashboard')


# Set Device Temperature
@login_required(login_url='login')
def set_temperature(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    if request.method == "POST":
        temperature = request.POST.get('temperature')
        try:
            device.temperature = int(temperature)
            device.save()
            messages.success(request, f"Temperature for '{device.name}' set to {temperature}")
        except ValueError:
            messages.error(request, 'Invalid temperature value')
    return redirect('dashboard')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        # print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)  # Delay saving to handle role assignment
                user.save()
                login(request, user)  # Automatically log the user in after registration
                return redirect('profile')  # Redirect to the profile page after successful registration
            except Exception as e:
                print(f"Error: {e}")
                form.add_error(None, "An error occurred during registration. Please try again.")
        else:
            # If the form is invalid, return the form with errors
            print(request.POST)
            print("Form is not valid:", form.errors)
    else:
        print("request.POST")
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Check if the selected role matches the user type
            if role == 'admin' and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            elif role == 'user' and not user.is_staff:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid role for the selected user.")
        else:
            messages.error(request, "Invalid username or password.")
        
    return render(request, 'login.html')




# Logout View (No login required)
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def user_dashboard(request):
    return render(request, 'accounts/profile.html')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserSettings
from django.contrib.auth.decorators import login_required

@login_required
def settings_view(request):
    user_settings, created = UserSettings.objects.get_or_create(MyUser=request.user)
    
    if request.method == "POST":
        user_settings.theme = request.POST.get("theme", "light")
        user_settings.notifications = request.POST.get("notifications") == "on"
        user_settings.energy_saving = request.POST.get("energy_saving") == "on"
        user_settings.security_mode = request.POST.get("security_mode") == "on"
        user_settings.temp_alerts = request.POST.get("temp_alerts") == "on"
        user_settings.save()
        return redirect("settings")
    
    return render(request, "settings.html", {"settings": user_settings})

@login_required
def update_settings_ajax(request):
    if request.method == "POST":
        user_settings, created = UserSettings.objects.get_or_create(MyUser=request.user)
        user_settings.theme = request.POST.get("theme", "light")
        user_settings.notifications = request.POST.get("notifications") == "true"
        user_settings.energy_saving = request.POST.get("energy_saving") == "true"
        user_settings.security_mode = request.POST.get("security_mode") == "true"
        user_settings.temp_alerts = request.POST.get("temp_alerts") == "true"
        user_settings.save()
        return JsonResponse({"status": "success", "message": "Settings updated successfully!"})
    return JsonResponse({"status": "error", "message": "Invalid request."})


def generate_password(shortcode, passkey, timestamp):
    """Generates M-Pesa API password using Base64 encoding."""
    password_str = shortcode + passkey + timestamp
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")







import cv2
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from ultralytics import YOLO
import numpy as np

# Load YOLOv8 Model
model = YOLO(r"static/automation.pt")  # Using the Nano model for efficiency


@csrf_exempt
def detect_objects(request):
    """
    API endpoint to upload an image and detect objects using YOLOv8.
    """
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        
        # Convert InMemoryUploadedFile to numpy array
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Check if image was loaded properly
        if image is None:
            return JsonResponse({"error": "Failed to decode image"}, status=400)

        # Perform Object Detection
        results = model(image)
        
        # Process results
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                confidence = round(box.conf[0].item(), 2)  # Confidence score
                label = model.names[int(box.cls[0])]  # Object class name

                detections.append({"label": label, "confidence": confidence, "coordinates": [x1, y1, x2, y2]})

                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"{label} ({confidence:.2f})"
                cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save processed image
        processed_image_path = f"media/detections/detected_{uploaded_file.name}"  # Fixed variable name
        cv2.imwrite(processed_image_path, image)

        return JsonResponse({"message": "Detection completed", "detections": detections, "image_url": processed_image_path})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests



from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

class ContactFormView(APIView):
    """
    API View to handle contact form submissions
    """
    def send_stylish_email(self, subject, recipient_email, template_type='admin', context=None):
        """
        Send a stylish HTML-formatted email
        
        :param subject: Email subject
        :param recipient_email: Recipient's email address
        :param template_type: 'admin' or 'confirmation'
        :param context: Additional context for the template
        """
        # Customize template based on type
        if template_type == 'admin':
            html_body = f"""
            <div class="info-row">
                <p><strong>New Contact Form Submission</strong></p>
            </div>
            <div class="info-row">
                <p><strong>Name:</strong> {context.get('name', 'N/A')}</p>
                <p><strong>Email:</strong> {context.get('sender_email', 'N/A')}</p>
            </div>
            <div class="info-row">
                <p><strong>Subject:</strong> {context.get('subject', 'No Subject')}</p>
                <p><strong>Message:</strong></p>
                <p>{context.get('message', 'No message content')}</p>
            </div>
            """
        else:  # confirmation
            html_body = f"""
            <div class="info-row">
                <p>Hello {context.get('name', 'Valued Visitor')},</p>
                <p>Thank you for reaching out through my portfolio contact form. Your message has been received and I will get back to you soon.</p>
            </div>
            <div class="info-row">
                <p><strong>Your Message Details:</strong></p>
                <p>Subject: {context.get('subject', 'No Subject')}</p>
            </div>
            <div class="info-row">
                <p>I appreciate you taking the time to connect. I look forward to our conversation.</p>
                <p>Best regards,<br>Your Portfolio Team</p>
            </div>
            """
        
        # Base HTML template with responsive design
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #4a4a4a;
                    color: white;
                    text-align: center;
                    padding: 15px;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    margin-top: 20px;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 0.8em;
                    color: #777;
                }}
                .info-row {{
                    margin-bottom: 10px;
                    padding: 10px;
                    background-color: #f9f9f9;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{subject}</h1>
                </div>
                <div class="content">
                    {html_body}
                </div>
                <div class="footer">
                    <p>© {datetime.now().year} Your Portfolio. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email with HTML content
        email = EmailMessage(
            subject=subject,
            body=full_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.content_subtype = 'html'  # Set content type to HTML
        email.send()

    def post(self, request):
        """
        Process contact form submission
        """
        
        # Extract and validate form data
        name = request.data.get('name', '').strip()
        sender_email = request.data.get('email', '').strip()
        subject = request.data.get('subject', '').strip()
        message = request.data.get('message', '').strip()

        # Basic validation
        if not all([name, sender_email, subject, message]):
            return Response({
                'message': 'All fields are required.',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Send admin notification email
            self.send_stylish_email(
                subject=f"Portfolio Contact: {subject}",
                recipient_email=settings.ADMIN_EMAIL,
                template_type='admin',
                context={
                    'name': name,
                    'sender_email': sender_email,
                    'subject': subject,
                    'message': message
                }
            )
            
            # Send confirmation to sender
            self.send_stylish_email(
                subject="Message Received - Portfolio Contact",
                recipient_email=sender_email,
                template_type='confirmation',
                context={
                    'name': name,
                    'subject': subject
                }
            )
            
            return Response({
                'message': 'Your message has been sent successfully.',
                'status': 'success'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Log the error in a production environment
            return Response({
                'message': 'Failed to send message. Please try again later.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class UserInteractionViewSet(viewsets.ModelViewSet):
#     queryset = UserInteraction.objects.all()
#     serializer_class = UserInteractionSerializer


# def pricing_view(request):
#     plans = [
#         {
#             'name': 'Basic Plan',
#             'price': '2500',
#             'color': '#20c997',
#             'icon': 'bi-box',
#             'features': [
#                 'Basic Security',
#                 'Limited Automation',
#                 'Email Support',
#                 {'text': 'No Voice Control', 'available': False},
#                 {'text': 'Limited Integrations', 'available': False},
#             ]
#         },
#         {
#             'name': 'Starter Plan',
#             'price': '5000',
#             'color': '#0dcaf0',
#             'icon': 'bi-send',
#             'featured': True,
#             'features': [
#                 'Advanced Automation',
#                 'Customizable Features',
#                 '24/7 Email Support',
#                 'Integration with Smart Devices',
#                 {'text': 'Limited Priority Support', 'available': False},
#             ]
#         },
#         {
#             'name': 'Business Plan',
#             'price': '8000',
#             'color': '#fd7e14',
#             'icon': 'bi-airplane',
#             'features': [
#                 'Full Automation',
#                 'Voice Assistant Integration',
#                 'Premium Support',
#                 'Advanced Analytics',
#                 'Extended Device Integration',
#             ]
#         },
#         {
#             'name': 'Ultimate Plan',
#             'price': '10000',
#             'color': '#0d6efd',
#             'icon': 'bi-rocket',
#             'features': [
#                 'All Features Included',
#                 'Dedicated Account Manager',
#                 'Priority Support',
#                 'Custom Smart Solutions',
#                 'Unlimited Integrations',
#             ]
#         },
#     ]
#     return render(request, 'pricing.html', {'plans': plans})


from django.shortcuts import render, redirect

def payment_success(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    context = {
        'plan': plan
    }
    return render(request, "payment_success.html", context)

def payment_failed(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    context = {
        'plan': plan
    }
    return render(request, "payment_failed.html", context)

from django.shortcuts import render, get_object_or_404
from .models import Plan

def payments(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    context = {
        'plan': plan
    }
    return render(request, 'payments.html', context)

import uuid
from django.urls import reverse
from .paystack import checkout
from django.contrib import messages
@login_required
def create_paystack_checkout_session(request, plan_id):
        plan = Plan.objects.get(id=plan_id)
        purchase_id = f"purchase_{uuid.uuid4()}"
        print("Plan ID:", plan.price)
        payment_success_url = f"/payment-success/{plan.id}/"
        callback_url = f"{request.scheme}://{request.get_host()}{payment_success_url}"
        checkout_data = {
       "email": request.user.email,
       "amount": int(plan.price) * 100,  # in kobo (₦2500)
       "currency": "KES",
       "channels": ["card", "bank_transfer", "bank", "ussd", "qr", "mobile_money"],
       "reference": purchase_id, # generated by developer
       "callback_url": callback_url,
       "metadata": {
           "product_id": plan_id,
           "user_id": request.user.id,
           "purchase_id": purchase_id,
       },
       "label": f"Checkout For {plan.name}"
   }
        status, check_out_session_url_or_error_message = checkout(checkout_data)
        if status:
            return redirect(check_out_session_url_or_error_message)
        else:
            messages.error(request, check_out_session_url_or_error_message)
        return redirect('payments')






