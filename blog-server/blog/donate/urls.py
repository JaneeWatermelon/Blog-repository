
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from donate.views import DonateView, DonateResultView

app_name = 'donate'

urlpatterns = [
    path('form', DonateView.as_view(), name='form'),
    path('result', DonateResultView.as_view(), name='result'),
]