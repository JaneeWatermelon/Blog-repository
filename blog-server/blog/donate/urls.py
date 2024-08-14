
from django.urls import include, path

from donate.views import DonateResultView, DonateView
from django.contrib.auth.decorators import login_required

app_name = 'donate'

urlpatterns = [
    path('form', login_required(DonateView.as_view()), name='form'),
    path('result', DonateResultView.as_view(), name='result'),
]