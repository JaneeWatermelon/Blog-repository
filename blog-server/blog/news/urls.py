
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from news.views import All_News_View, change_category

app_name = 'news'

urlpatterns = [
    path('change_category', change_category, name='change_category')
]