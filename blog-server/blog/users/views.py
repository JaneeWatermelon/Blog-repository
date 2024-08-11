from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from users.forms import ProfileForm, UserAuthForm, UserRegistrationForm
from users.models import User, EmailVerification
from news.models import News

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from news.views import ajax_login_required


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    title = 'Registration Page'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'

class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/verification_email.html'
    title = 'Email Verification Page'

    def get_context_data(self, **kwargs):
        context = super(EmailVerificationView, self).get_context_data()
        user = User.objects.get(email=kwargs['email'])
        context['is_verified'] = user.is_verified
        return context
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        record = EmailVerification.objects.filter(code=code, user=user)
        if record.exists() and record.first().is_expired() == False:
            user.is_verified = True
            user.save()
        return super(EmailVerificationView, self).get(request, *args, **kwargs)




class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    template_name = 'users/auth.html'
    form_class = UserAuthForm
    title = 'Registration Page'
    success_message = 'Поздравляем! Вы успешно вошли!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))
@login_required
def UserLogout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('all_news'))
@login_required
def UserProfileView(request, pk):
    user = request.user
    if request.method == "POST":
        if request.FILES:
            if user.image.name != 'profilo.jpg':
                user.image.delete(save=False)
            dot_index = request.FILES['image'].name.rfind('.')
            request.FILES['image'].name = f"{request.user.id}{request.FILES['image'].name[dot_index:]}"
        form = ProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile', args=(pk,)))
        else:
            print(form.errors)
    else:
        request.session.setdefault('type', 'like')
        print(request.session['type'])
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
        }
        return render(request, 'users/profile.html', context)
@ajax_login_required
def see_news_in_profile(request):
    if request.method == "GET":
        profile_news_type = request.GET['type']

        if profile_news_type == 'like':
            request.session['type'] = 'like'
        elif profile_news_type == 'view':
            request.session['type'] = 'view'
        else:
            request.session['type'] = 'none'
        print(request.session['type'])
        data = {
            'type': profile_news_type
        }
        return JsonResponse(data)


