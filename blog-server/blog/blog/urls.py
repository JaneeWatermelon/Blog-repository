from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from news.views import (All_News_View,
                        clear_hearts_from_users_and_news,
                        try_get_key_words,
                        parsing_playground_games,
                        parsing_womanhit,
                        fill_categories,)

static_urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', All_News_View.as_view(), name='all_news'),
    path('news/', include('news.urls', namespace='news')),
    path('donate/', include('donate.urls', namespace='donate')),
    path('users/', include('users.urls', namespace='users')),
    path('', include(static_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path('parsing/', parsing_playground_games, name='parsing')]
    urlpatterns += [path('clear_hearts/', clear_hearts_from_users_and_news, name='clear_hearts')]
    urlpatterns += [path('try_words/', try_get_key_words, name='try_words')]
    urlpatterns += [path('fill_categories/', fill_categories, name='fill_categories')]
