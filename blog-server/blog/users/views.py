from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import ProfileForm, UserAuthForm, UserRegistrationForm
from users.models import User
from news.models import News

from django.http import JsonResponse


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

class UUserProfileView(TitleMixin, UpdateView):
    model = User
    title = 'Profile Page'
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

def UserProfileView(request, pk):
    user = request.user
    if request.method == "POST":
        if request.FILES:
            user.image.delete()
            user.save()
            dot_index = request.FILES['image'].name.rfind('.')
            request.FILES['image'].name = f"{request.user.id}{request.FILES['image'].name[dot_index:]}"
        form = ProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile', args=(pk,)))
        else:
            print(form.errors)
    else:
        liked_news = News.objects.filter(pk=0)
        viewed_news = News.objects.filter(pk=0)
        for like_id in user.liked_news_id:
            liked_news = liked_news.union(News.objects.filter(pk=like_id))
        for view_id in user.viewed_news_id:
            viewed_news = viewed_news.union(News.objects.filter(pk=view_id))
        context = {
            'form': ProfileForm(instance=request.user),
            'liked_news': liked_news,
            'viewed_news': viewed_news,
            'object_list': liked_news,
            'type': 'like',
        }
        return render(request, 'users/profile.html', context)

def see_news_in_profile(request):
    if request.method == "GET":
        profile_news_type = request.GET['type']
        profile_view = UserProfileView(request=request)
        if profile_news_type == 'like':
            profile_view['object_list'] = profile_view['liked_news']
            profile_view['type'] = profile_view['like']
        elif profile_news_type == 'view':
            profile_view['object_list'] = profile_view['viewed_news']
            profile_view['type'] = profile_view['view']
        else:
            profile_view['type'] = profile_view['none']
        data = {
            'type': profile_news_type
        }
        return JsonResponse(data)


