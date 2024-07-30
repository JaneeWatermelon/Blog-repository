from django import forms
from users.models import User

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type your name'
    })),
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type your surname'
    })),
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Come up with a username'
    })),
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Type your email'
    })),
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Come up with a password'
    })),
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat your password'
    })),

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

from django import forms
from users.models import User

class AuthForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Come up with a username'
    })),
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat your password'
    })),

    class Meta:
        model = User
        fields = ['username', 'password']
