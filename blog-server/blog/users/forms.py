import uuid

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.timezone import now, timedelta

from users.models import EmailVerification, User
from users.tasks import send_email_task


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

    def save(self, commit=True):
        user = super().save()
        print('before send')
        send_email_task.delay(user.id)
        print('after send')
        return user

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
        'id': 'new_avatar',
        'onchange': 'readURL(this);',
        'style': 'position: absolute; opacity: 0; cursor: pointer;'
    }), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'image']
