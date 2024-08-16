
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from news.views import (All_News_View, clear_hearts_from_users_and_news,
                        parsing_genshin, try_get_key_words,
                        parsing_playground_movies,
                        parsing_playground_hardware,
                        parsing_playground_games,
                        parsing_womanhit,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', All_News_View.as_view(), name='all_news'),
    path('news/', include('news.urls', namespace='news')),
    path('donate/', include('donate.urls', namespace='donate')),
    path('users/', include('users.urls', namespace='users')),

    path('parsing/', parsing_womanhit, name='parsing'),
    path('clear_hearts/', clear_hearts_from_users_and_news, name='clear_hearts'),
    path('try_words/', try_get_key_words, name='try_words'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
