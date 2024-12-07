from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from rest_framework import status

from .models import Device, UserPreferences, Payment
from .forms import CustomUserCreationForm, EmailAuthenticationForm, PaymentForm
from django.db import IntegrityError
from django.db.models import Sum
from .forms import UserPreferencesForm
from .serializers import PaymentSerializer


# Helper function to generate insights based on device usage
def generate_device_insights(devices):
    insights = []
    for device in devices:
        # Check if total_usage_time is greater than 5 hours (3600 * 5 seconds)
        if device.total_usage_time and device.total_usage_time.total_seconds() > 3600 * 5:
            insights.append(f"Device '{device.name}' is used for more than 5 hours daily.")
        # Check if the device is turned off
        if not device.status:
            insights.append(f"Device '{device.name}' is currently turned off.")
    return insights


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


# API Endpoint for Real-Time Device Data
@login_required(login_url='login')
def fetch_device_data(request):
    devices = Device.objects.filter(user=request.user)
    device_data = [
        {
            'id': device.id,
            'name': device.name,
            'status': device.status,
            'total_usage_time': str(device.total_usage_time),
        }
        for device in devices
    ]
    return JsonResponse({'devices': device_data})


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


# Home View
def home(request):
    if request.user.is_authenticated:
        user = request.user  # You can now pass the user object directly to the template
    else:
        user = None
    return render(request, 'home.html', {'user': user})


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('profile')
            except IntegrityError:
                messages.error(request, 'This username is already taken. Please choose a different one.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to profile if already logged in

    next_url = request.GET.get('next', 'profile')  # Default to 'profile' if no `next` parameter is provided

    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(next_url)  # Redirect to intended page
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})



# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


# Toggle Device Status
@login_required(login_url='login')
def toggle_device(request, device_id):
    device = get_object_or_404(Device, id=device_id, user=request.user)

    now = datetime.now()
    if device.status:  # Device is being turned off
        if device.last_used:
            usage_time = now - device.last_used
            device.total_usage_time += usage_time

    # Toggle device status
    device.status = not device.status
    device.last_used = now if device.status else None
    device.save()

    # Display success message
    messages.success(request, f"Device '{device.name}' status updated to {'ON' if device.status else 'OFF'}.")
    return redirect('accounts/dashboard')


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


# Profile View
@login_required(login_url='login')
def profile_view(request):
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(request, 'accounts/profile.html', {'form': form})


# Form Submission Handler for Contact Form
def submit_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data (e.g., save it or send an email)
            return redirect('success')  # Replace with a success page URL
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# Test Login (For debugging purposes)
def test_login(request):
    return render(request, 'accounts/login.html')


import redis

# Initialize the Redis connection
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatHistory, Device
import redis  # Ensure Redis is installed and configured

# Initialize Redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
from .chatbot import get_bot_response  # Import your chatbot logic

def get_bot_response(user_message):
    # Simple chatbot logic for now
    if "hello" in user_message.lower():
        return "Hi there! How can I help you today?"
    elif "bye" in user_message.lower():
        return "Goodbye! Have a nice day."
    return "I'm sorry, I don't understand that."

from .models import ChatHistory

import redis

# Redis configuration (adjust if needed)
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def chatbot_view(request):
    """
    Chatbot API view for handling user messages and responding dynamically.
    """
    if request.method == "POST":
        user_message = request.POST.get("message")
        if not user_message:
            return JsonResponse({"error": "Message content is required."}, status=400)

        # Get a dynamic response from the chatbot logic
        bot_response = get_bot_response(user_message)

        # Optionally save the user message to Redis for session-based persistence
        session_id = request.session.session_key or request.session.create()
        r.hset(session_id, "last_user_message", user_message)
        r.hset(session_id, "last_bot_response", bot_response)

        # Save the chat history to the database
        chat_entry = ChatHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,  # Optional user association
            user_message=user_message,
            bot_response=bot_response,
            message_type='user',  # Could dynamically set based on whether it's a bot or user
            status='success',  # Adjust status dynamically if needed
            session_id=session_id,  # Store the session ID here
        )

        return JsonResponse({
            "response": bot_response,
            "session_id": session_id  # Returning session_id so it can be tracked in the frontend
        })

    # Handle GET requests (i.e., render the chatbot page)
    return render(request, 'chatbot.html')


from django.views.decorators.csrf import csrf_exempt
from .chatbot import get_bot_response  # Import your chatbot logic


@csrf_exempt  # Exempt CSRF for AJAX requests if you're testing locally
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')  # Get the user's message

        if user_message:
            bot_response = get_bot_response(user_message)  # Process the message with chatbot logic
            return JsonResponse({'bot_response': bot_response})  # Send back the bot's response

        return JsonResponse({'error': 'No message provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def pricing_plans(request):
    plans = PricingPlan.objects.prefetch_related('features').all()

    return render(request, 'pricing.html', {'plans': plans})



def purchase(request, plan_id):
    # Get the selected pricing plan
    plan = get_object_or_404(PricingPlan, id=plan_id)

    # Here, you can handle the logic to add the plan to a cart or initiate a payment gateway.
    # For now, we'll just render a confirmation page with the selected plan.
    return render(request, 'purchase.html', {'plan': plan})


import requests
from django.contrib import messages
from django.conf import settings
from django.views.generic.edit import CreateView


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'

    def form_valid(self, form):
        # Save the payment instance
        payment = form.save(commit=False)
        plan_id = self.kwargs.get('plan_id')
        plan = get_object_or_404(PricingPlan, id=plan_id)
        payment.plan = plan
        payment.save()

        # Trigger M-Pesa STK Push
        phone_number = form.cleaned_data['phone_number']
        amount = plan.price
        response = self.initiate_stk_push(phone_number, amount)

        if response.get('ResponseCode') == '0':
            # Success: STK Push sent to the user's phone
            messages.success(self.request, "Payment request sent to your phone. Complete the process to proceed.")
        else:
            # Failure: Display the error message
            error_message = response.get('errorMessage', 'Unable to process payment.')
            messages.error(self.request, f"Payment failed: {error_message}")

        return super().form_valid(form)

    def initiate_stk_push(self, phone_number, amount):
        """
        Initiate M-Pesa STK Push
        """
        # M-Pesa credentials from settings
        consumer_key = 'NGfT01CB9Flb9mtWjZeXBGw3MRglmPy4PqOuHyIqWHPkA379'
        consumer_secret = 'uZFQ30MlDSTdgOddOH4X7fr3viiAD5eiPnPdQSEhD2oIYbWxYVA1ANOBkf5VkhQR'
        business_shortcode = '174379'
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        callback_url = settings.MPESA_CALLBACK_URL

        # Generate Access Token
        token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        token_response = requests.get(token_url, auth=(consumer_key, consumer_secret))
        access_token = token_response.json().get('access_token')

        # Generate Timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Password for the STK Push
        password = f"{'174379'}{'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'}{timestamp}".encode('ascii').hex()

        # STK Push Payload
        stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        payload = {
            "BusinessShortCode": '174379',
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 2500,
            "PartyA": '+254 793595836',  # Customer phone number
            "PartyB": '174379',  # PayBill or Till Number
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": "Plan Payment",
            "TransactionDesc": "Payment for Plan"
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Make API Call
        response = requests.post(stk_push_url, json=payload, headers=headers)
        return response.json()




def payment_callback(request):
    """
    Callback endpoint to handle M-Pesa payment status.
    """
    if request.method == 'POST':
        # Safaricom sends POST request with payment details
        callback_data = request.POST

        # Extract relevant information from the callback data
        transaction_id = callback_data.get('CheckoutRequestID')
        payment_status = callback_data.get('ResultCode')  # ResultCode = 0 means successful payment

        # Handle missing or incorrect callback data
        if not transaction_id or payment_status is None:
            return JsonResponse({'error': 'Invalid callback data'}, status=400)

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)

        # Check payment status and update the payment record accordingly
        if payment_status == '0':  # M-Pesa payment was successful
            payment.status = 'SUCCESS'
            payment.save()
            return render(request, 'payment_status.html', {
                'status': 'success',
                'payment': payment
            })
        else:  # Payment failed
            payment.status = 'FAILED'
            payment.save()
            return render(request, 'payment_status.html', {
                'status': 'failed',
                'payment': payment
            })

    # If the method is not POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.views.generic import ListView, CreateView
from .models import PricingPlan  # Assuming you have a PricingPlan model

class PlanListView(ListView):
    model = PricingPlan
    template_name = 'plan_list.html'
    context_object_name = 'plans'


from django.http import JsonResponse


def plan_payment_api(request):
    # Example logic for listing and creating payments
    if request.method == 'GET':
        payments = Payment.objects.all()
        payment_data = [{"transaction_id": payment.transaction_id, "status": payment.status} for payment in payments]
        return JsonResponse(payment_data, safe=False)

    elif request.method == 'POST':
        # Logic for creating a payment (this is just an example)
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        payment = Payment.objects.create(transaction_id=transaction_id, amount=amount, status='PENDING')
        return JsonResponse({"message": "Payment created", "payment_id": payment.id}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



from .models import Payment


def payment_status_view(request, payment_id):
    # Fetch the payment based on the payment_id
    payment = get_object_or_404(Payment, id=payment_id)

    # Determine the status (this can depend on the payment model or callback data)
    if payment.status == 'SUCCESS':
        status = 'success'
    elif payment.status == 'PENDING':
        status = 'pending'
    else:
        status = 'failed'

    # Pass the necessary context to the template
    return render(request, 'payment_status.html', {
        'status': status,
        'transaction_id': payment.transaction_id,
        'pricing_plan': payment.pricing_plan,  # Access the PricingPlan here
    })


from django.shortcuts import render, get_object_or_404, redirect
from .forms import PaymentForm
import requests  # Assuming you would use this to interact with the M-Pesa API


def payment_view(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            confirmation_code = form.cleaned_data.get('confirmation_code', None)
            password = form.cleaned_data['password']  # Get the password (M-Pesa PIN) from the form

            # Call the M-Pesa API to initiate payment
            success = initiate_mpesa_payment(phone_number, plan.price, confirmation_code)

            if success:
                return redirect('payment-success')  # Redirect to a success page after payment
            else:
                form.add_error(None, 'Payment failed. Please try again.')

    else:
        form = PaymentForm()

    return render(request, 'payment_form.html', {'form': form, 'plan': plan})


# def initiate_mpesa_payment(phone_number, amount, confirmation_code=None, password=None):
#     # Example of initiating a payment via M-Pesa API
#     # You would replace this with actual code to interact with the M-Pesa API
#     payload = {
#         'phone_number': phone_number,
#         'amount': amount,
#         'confirmation_code': confirmation_code,  # Optional, based on your workflow
#     }
#
#     # Example API request (you need to replace this with the actual M-Pesa API details)
#     response = requests.post('https://api.safaricom.co.ke/mpesa/payment', data=payload)
#
#     if response.status_code == 200:
#         return True
#     return False


from rest_framework.decorators import api_view
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def paymentsapi(request, id=None):
    if request.method == 'GET':
        # Retrieve all payments or a specific payment by ID
        if id:
            payment = get_object_or_404(Payment, id=id)
            serializer = PaymentSerializer(payment)
        else:
            payment = Payment.objects.all()
            serializer = PaymentSerializer(payment, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # Create a new payment record
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Update an existing payment record
        payment = get_object_or_404(Payment, id=id)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a specific payment record
        payment = get_object_or_404(Payment, id=id)
        payment.delete()
        return JsonResponse({'message': 'Payment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def mpesaapi(request):
    client = MpesaClient()
    phone_number = '0793595836'
    amount = 1
    account_reference = 'eMobilis'
    transaction_desc = 'Payment for Web Dev'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'
    response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


import json
import io
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
from pydub import AudioSegment
import openai
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from django.conf import settings


starting_prompt = "TYPE YOUR PROJECT DETAILS BASED TO TRAIN GPT"

# Set up logger
logger = logging.getLogger(__name__)

class ChatBotView(APIView):

    def post(self, request, user_id=None):
        """
        Handles incoming requests for chatbot communication via text or audio.
        """
        chat_history = self.audio_conversion(request)
        chat_type = request.data.get('chat_type')
        user = request.data.get('user_id')
        text = request.data.get('user_chat')

        if chat_type != 'text' and isinstance(chat_history, Response):
            return chat_history

        if chat_type == 'text':
            serializer = ChatHistorySerializer(data=request.data)
            chat_history = self.serializer_valid_check(serializer, request.data)
            if isinstance(chat_history, Response):
                return chat_history

        if chat_type == 'audio':
            audio_file = open(chat_history.audio.path, "rb")
            try:
                transcript = openai.Audio.transcriptions.create(model="whisper-1", file=audio_file)
                text = transcript['text']
                chat_history.user_chat = text
                chat_history.save()
            except Exception as e:
                logger.error(f"Error in transcription: {e}")
                return Response({"error": "Audio transcription failed."}, status=400)

        # Retrieve previous chat history
        chat_historys = ChatHistory.objects.filter(user_id__id=user)
        messages = self.chat_text(chat_historys, starting_prompt)

        # Get response from GPT
        translation = self.translated_data(messages)

        if isinstance(translation, Response):
            return translation

        chat_history.response_chat = translation
        chat_history.save()

        # Serialize and return response
        serializer = ChatHistorySerializer(instance=chat_history)
        logger.info(f"Chat response: {serializer.data}")
        return Response(serializer.data, status=200)

    def get(self, request, user_id):
        """
        Fetch chat history for a specific user.
        """
        chat_history = ChatHistory.objects.filter(user_id__id=user_id)
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data)

    def delete(self, request, user_id):
        """
        Delete chat history for a specific user.
        """
        ChatHistory.objects.filter(user_id__id=user_id).delete()
        return Response({})

    def chat_text(self, chat_historys, starting_prompt):
        """
        Prepares the messages for GPT, including the starting prompt and previous chat history.
        """
        messages = [{"role": "system", "content": starting_prompt}]
        if chat_historys:
            for chat_history in chat_historys:
                if chat_history.user_chat:
                    messages.append({"role": "user", "content": chat_history.user_chat})
                if chat_history.response_chat:
                    messages.append({"role": "system", "content": chat_history.response_chat})
        return messages

    def serializer_valid_check(self, serializer, data):
        """
        Validates and saves the serializer.
        """
        if serializer.is_valid():
            return serializer.save()
        else:
            logger.error(f"Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=400)

    def translated_data(self, messages):
        """
        Get the chatbot response from GPT-4.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Check model availability
                messages=messages
            )
            message = response.choices[0].message['content']
            logger.info(f"OpenAI response: {message}")
            return message
        except Exception as e:
            logger.error(f"Error in GPT API call: {e}")
            return Response({"error": "Error generating response from GPT."}, status=500)

    def audio_conversion(self, request):
        """
        Converts the uploaded audio file to an MP3 format if the input is audio.
        """
        audio_file = request.data.get('audio', None)
        chat_type = request.data.get('chat_type', None)

        if chat_type == 'audio' and audio_file:
            try:
                # Read audio file and convert it
                audio_content = audio_file.read()
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_content), format="wav")
                modified_audio_content = audio_segment.export(format="mp3").read()
                modified_audio_file = ContentFile(modified_audio_content, name=f'{audio_file.name}.mp3')

                # Create ChatHistory instance with the modified audio
                data = request.data.copy()
                data['audio'] = modified_audio_file
                serializer = ChatHistorySerializer(data=data)

                if serializer.is_valid():
                    return serializer.save()
                else:
                    logger.error(f"Audio conversion failed: {serializer.errors}")
                    return Response(serializer.errors, status=400)

            except Exception as e:
                logger.error(f"Error processing audio file: {e}")
                return Response({"error": "Failed to process audio file."}, status=400)
        else:
            return Response({"error": "No audio file found or incorrect chat type."}, status=400)
