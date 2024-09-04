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
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': 'Введите фамилию',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'placeholder': 'Придумайте имя пользователя',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form_input',
        'placeholder': 'Введите адрес электронной почты',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': 'Придумайте пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': 'Повторите пароль',
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
        'class': 'form_input',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_input',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form_input',
    }))
    last_name = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form_input',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_input',
        'readonly': True,
        'style': 'color: rgba(var(--dark-font), 0.5);',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form_input',
        'readonly': True,
        'style': 'color: rgba(var(--dark-font), 0.5);',
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
