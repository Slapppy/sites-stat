from django import forms
from .models import Counter
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class AddCounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = ["name", "link"]


class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=40)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=70)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "surname", "email"]
