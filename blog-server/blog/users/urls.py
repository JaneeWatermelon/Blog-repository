
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from users.views import UserLoginView, UserRegistrationView, UserLogout, UserProfileView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout, name='logout'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
]
