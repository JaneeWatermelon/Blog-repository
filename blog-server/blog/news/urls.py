from django.urls import include, path

from news.views import (All_News_View, Full_Card_View, New_News_View,
                        Popular_News_View, Recommended_News_View,
                        change_category, change_star, check_view, heart_news,
                        leave_comment, rate_comment, change_show_type)

app_name = 'news'


urlpatterns = [
    path('all/page/<int:page>', All_News_View.as_view(), name='paginator_all'),
    path('recommended', Recommended_News_View.as_view(), name='recommended'),
    path('recommended/page/<int:page>', Recommended_News_View.as_view(), name='paginator_recommended'),
    path('popular', Popular_News_View.as_view(), name='popular'),
    path('popular/page/<int:page>', Popular_News_View.as_view(), name='paginator_popular'),
    path('new', New_News_View.as_view(), name='new'),
    path('new/page/<int:page>', New_News_View.as_view(), name='paginator_new'),
    path('full_card/<int:pk>', Full_Card_View.as_view(), name='full_card'),

    path('change_category', change_category, name='change_category'),
    path('change_star', change_star, name='change_star'),
    path('like_news', heart_news, name='like_news'),
    path('rate_comment', rate_comment, name='rate_comment'),
    path('leave_comment', leave_comment, name='leave_comment'),
    path('check_view', check_view, name='check_view'),
    path('change_show_type', change_show_type, name='change_show_type'),
]