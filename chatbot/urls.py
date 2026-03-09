# chatbot/urls.py
from django.urls import path
from . import views

app_name = 'chatbot'
urlpatterns = [
    path('', views.chatbot_interface, name='chatbot_get'),
    # path('chat/', views.chat_api, name='chat_api'),  # Add this line
    path('api/', views.chat_handler, name='api'),
]

