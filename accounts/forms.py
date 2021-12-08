from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserUniqueId

class SignUpForm(UserCreationForm):
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('username','image', 'email', 'password1', 'password2')
