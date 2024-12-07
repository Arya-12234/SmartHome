from django.contrib import admin
from django.urls import path

from . import views
from .views import PlanListView, PaymentCreateView, chatbot_view, ChatBotView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('preferences/', views.update_preferences, name='preferences'),
    path('', views.home, name='home'),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing_plans, name='pricing_plans'),
    path('purchase/<int:plan_id>/', views.purchase, name='purchase'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),  # Use the class-based view for payment
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('plans/', PlanListView.as_view(), name='plan_list'),
    path('payment/<int:plan_id>/', views.payment_view, name='payment'),  # Adjusted if you're using the function-based view for payment
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/<int:payment_id>/', views.payment_status_view, name='payment_status'),
    path('api/payment/', views.plan_payment_api, name='payment_api'),  # For listing and creating payments
    path('api/payment/<int:payment_id>/', views.plan_payment_api, name='payment_api_detail'),  # For updating or deleting a specific payment    # Ensure this is handling the M-Pesa callback correctly
    path('submit/', views.submit_form, name='submit_form'),
    path('paymentsapi/', views.paymentsapi, name='paymentsapi'),
    path('toggle_device/<int:device_id>/', views.toggle_device, name='toggle_device'),
    path('set_brightness/<int:device_id>/', views.set_brightness, name='set_brightness'),
    path('set_temperature/<int:device_id>/', views.set_temperature, name='set_temperature'),
    path('test-login/', views.test_login, name='test_login'),
    path('chatbot/', views.chatbot_view, name='chatbot_view'),
    path('chat-bot/', views.ChatBotView.as_view(), name='chat-bot'),
]
from django.urls import path
from . import consumers

# WebSocket URL pattern
websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]

