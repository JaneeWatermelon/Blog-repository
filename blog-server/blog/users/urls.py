
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from users.views import (UserLoginView, UserLogout, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout, name='logout'),
    path('profile/<int:pk>', login_required(UserProfileView), name='profile'),
]
