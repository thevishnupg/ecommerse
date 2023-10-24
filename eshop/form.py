from django import forms
from .models import ShippingAddress

# Authentication form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']