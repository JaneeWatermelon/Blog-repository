from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import ProfileForm, UserAuthForm, UserRegistrationForm
from users.models import User


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    title = 'Registration Page'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'

class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    template_name = 'users/auth.html'
    form_class = UserAuthForm
    title = 'Registration Page'
    success_message = 'Поздравляем! Вы успешно вошли!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))

def UserLogout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('all_news'))

class UserProfileView(TitleMixin, UpdateView):
    model = User
    title = 'Profile Page'
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


