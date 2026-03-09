from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView, RoomListCreateView, RoomRetrieveUpdateDeleteView, DeviceListCreateView, DeviceRetrieveUpdateDeleteView, settings_view, update_settings_ajax, payment_failed,  payment_success
from rest_framework_simplejwt.views import TokenRefreshView

from automation import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("rooms/", RoomListCreateView.as_view(), name="room-list-create"),
    path("room/",views.room_view, name="room"),
    path("devices/", views.devices_view, name="devices"),
    path("rooms/<int:pk>/", RoomRetrieveUpdateDeleteView.as_view(), name="room-detail"),
    path("devices/", DeviceListCreateView.as_view(), name="device-list-create"),
    path("devices/<int:pk>/", DeviceRetrieveUpdateDeleteView.as_view(), name="device-detail"),
    path('preferences/', views.update_preferences, name='preferences'),
    path('', views.home, name='home'),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    # path('pricing/', pricing_view, name='pricing'),
    path('payment-success/<int:plan_id>/', views.payment_success, name='payment_success'),
    path('payment-failed/<int:plan_id>/', views.payment_failed, name='payment_failed_view'),
    path('payments/<int:plan_id>/', views.payments, name='payments'),
    path('checkout/<int:plan_id>/', views.create_paystack_checkout_session, name='checkout-plan'),


    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('set_brightness/<int:device_id>/', views.set_brightness, name='set_brightness'),
    path('set_temperature/<int:device_id>/', views.set_temperature, name='set_temperature'),
    path('settings/', settings_view, name='settings'),
    path('settings/update/', update_settings_ajax, name='update_settings_ajax'),
    # path("payment", views.payments),
    path("detection/", views.detect_objects, name="detect_objects"),
    path('api/contact/', views.ContactFormView.as_view(), name='contact_form_api'),

    # router.register(r'interactions', UserInteractionViewSet)


]

