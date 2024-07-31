from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': 'Type your name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': 'Type your surname',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': 'Come up with a username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form_input',
        'placeholder': 'Type your email',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': 'Come up with a password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': 'Repeat your password',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Come up with a username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat your password'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': True,
        'style': 'color: rgba(0, 0, 0, 0.6);',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'readonly': True,
        'style': 'color: rgba(0, 0, 0, 0.6);',
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'profile_info_photo',
        'style': 'position: absolute; opacity: 0;'
    }), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'image']
