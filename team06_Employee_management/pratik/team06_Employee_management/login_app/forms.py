from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import time


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

def greeting_fun():
    current_hour = time.localtime().tm_hour

    # Determine the appropriate greeting
    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 17:
        return "Good Afternoon"
    elif 17 <= current_hour < 21:
        return "Good Evening"
    else:
        return "Good Night"
