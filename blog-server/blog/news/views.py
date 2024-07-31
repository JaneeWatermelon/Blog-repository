from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import JsonResponse

from django.urls import reverse, reverse_lazy

from common.views import TitleMixin
from news.models import News, Category

import requests
from bs4 import BeautifulSoup
import fake_useragent


class All_News_View(TitleMixin, ListView):
    template_name = "news/all_news.html"
    title = 'All News'
    model = News
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.filter(pk=0)
        active_categories = self.request.session.setdefault('active_categories', [])
        if active_categories:
            for category_id in active_categories:
                result = result.union(queryset.filter(category=Category.objects.get(pk=category_id)))
            return result.order_by('-id')
        else:
            return queryset.order_by('-id')
    def reload_queryset(self):
        self.object_list = self.get_queryset()

def change_category(request):
    if request.method == 'GET':
        category_id = request.GET.get('id', 'zero')
        active_categories = request.session.setdefault('active_categories', [])

        if category_id == 'zero':
            active_categories = []
        elif int(category_id) not in active_categories:
            active_categories.append(int(category_id))
        else:
            active_categories.remove(int(category_id))
        request.session['active_categories'] = active_categories
        print(active_categories)
        data = {
            'active_categories': active_categories
        }
        current_list_view = All_News_View(request=request)
        current_list_view.reload_queryset()
        return JsonResponse(data)

def parsing_news(request):
    link = 'https://genshin.hoyoverse.com/ru/news'
    response = requests.get(link)
    print('done')

    soup = BeautifulSoup(response.text, 'lxml').find('div', id='frame')
    print(soup.text)
    news_ul = soup.find('ul', class_='news')
    print(news_ul)
    all_news = soup.find_all('li', class_=['news__item', 'news__tag-2'])
    print(all_news)
    print(len(all_news))
    for news in all_news:
        print('in for')
        content = news.find('a', class_='news__title news__content ellipsis')
        name = content.find('h3').text
        description = content.find('p').text
        result_news = News(
            name=name,
            description=description,
            url='https://genshin.hoyoverse.com/ru/news',
            category=Category.objects.all().first()
        )
        print('before save')
        result_news.save()
        print('after save')
    return HttpResponseRedirect(reverse('all_news'))


