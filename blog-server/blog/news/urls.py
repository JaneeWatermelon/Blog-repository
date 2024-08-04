
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from news.views import (All_News_View, Full_Card_View, change_category,
                        change_star, heart_news, leave_comment, rate_comment)

app_name = 'news'

urlpatterns = [
    path('all/page/<int:page>', All_News_View.as_view(), name='paginator_all'),
    path('full_card/<int:pk>', Full_Card_View.as_view(), name='full_card'),
    path('change_category', change_category, name='change_category'),
    path('change_star', change_star, name='change_star'),
    path('like_news', heart_news, name='like_news'),
    path('rate_comment', rate_comment, name='rate_comment'),
    path('leave_comment', leave_comment, name='leave_comment'),
]