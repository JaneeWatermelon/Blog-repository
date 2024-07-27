from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from common.views import TitleMixin
# Create your views here.
class All_News_View(TitleMixin, TemplateView):
    template_name = "users/profile.html"
    title = 'All News'
