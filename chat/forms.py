# chat/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "gender", "birth_date", "password1", "password2")
