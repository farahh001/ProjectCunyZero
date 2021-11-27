from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','image', 'email', 'password1', 'password2')