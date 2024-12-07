from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import UserPreferences, ChatHistory



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, required=True)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = [
            'lighting_day',
            'lighting_night',
            'security_alarm',
            'security_curtains',
            'security_gate',
            'heating_shower',
        ]
        widgets = {
            'lighting_day': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
            'lighting_night': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
            'security_alarm': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
            'security_curtains': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
            'security_gate': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
            'heating_shower': forms.Select(choices=[('on', 'On'), ('off', 'Off')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})






from django import forms

class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your M-Pesa phone number'}))
    confirmation_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter confirmation code (optional)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter M-Pesa PIN'}))  # Password field for M-Pesa PIN

# Chatbot Interaction Form
class ChatbotForm(forms.Form):
    message = forms.CharField(
        label="Your Message",
        max_length=500,
        widget=forms.Textarea(attrs={
            "placeholder": "Type your message...",
            "rows": 3,
            "class": "form-control"
        }),
    )




from django import forms
from .models import ChatHistory, Device

class ChatHistoryForm(forms.ModelForm):
    class Meta:
        model = ChatHistory
        fields = [
            'user',
            'user_message',
            'bot_response',
            'device',
            'command',
            'status',
            'error_details'
        ]
        widgets = {
            'user_message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'bot_response': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'status': forms.Select(choices=ChatHistory.STATUS_CHOICES),
        }

    # Optionally, you can add custom validation or clean methods
    def clean_user_message(self):
        user_message = self.cleaned_data.get('user_message')
        if not user_message:
            raise forms.ValidationError('User message cannot be empty')
        return user_message

    def clean_bot_response(self):
        bot_response = self.cleaned_data.get('bot_response')
        if not bot_response:
            raise forms.ValidationError('Bot response cannot be empty')
        return bot_response

    def clean_device(self):
        device = self.cleaned_data.get('device')
        if not device:
            raise forms.ValidationError('Device is required')
        return device
