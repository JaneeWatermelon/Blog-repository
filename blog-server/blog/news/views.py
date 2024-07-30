from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from common.views import TitleMixin

from news.models import News

class All_News_View(TitleMixin, ListView):
    template_name = "news/all_news.html"
    title = 'All News'
    model = News
    paginate_by = 30


