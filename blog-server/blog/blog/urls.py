"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from news.views import All_News_View, parsing_news
from users.views import change_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', All_News_View.as_view(), name='all_news'),
    path('news/', include('news.urls', namespace='news')),
    path('donate/', include('donate.urls', namespace='donate')),
    path('users/', include('users.urls', namespace='users')),
    path('parsing/', parsing_news, name='parsing'),
    path('change_user/', change_user, name='change_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
