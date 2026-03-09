from django import forms

from .models import MyUser, UserPreferences


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

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please choose a different one.")
        return email



from django import forms
from django.contrib.auth import get_user_model

class EmailAuthenticationForm(forms.Form):
    username = forms.EmailField(label='Email')  # Use email field
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        email = self.cleaned_data.get('username')
        User = get_user_model()

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email address.")
        return email




