# forms.py
from django import forms
from .models import LoginAttempt

from django import forms

class PlainTextLoginForm(forms.Form):
    email = forms.EmailField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)
