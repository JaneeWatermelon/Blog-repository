import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common.views import TitleMixin
from news.models import Category, Comment, News
from users.models import User


class All_News_View(TitleMixin, ListView):
    template_name = "news/all_news.html"
    title = 'All News'
    model = News
    paginate_by = 3

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

class Full_Card_View(TitleMixin, DetailView):
    model = News
    title = 'Detail News'
    template_name = 'news/full_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(news=self.object)
        return context

def heart_news(request):
    if request.method == 'GET':
        user = request.user

        news_id = int(request.GET['id'][5:])
        news = News.objects.get(pk=news_id)
        print('got preference')

        if news_id in user.liked_news_id:
            print('in if')
            news.likes -= 1
            user.liked_news_id.remove(news_id)
        else:
            print('in else')
            news.likes += 1
            user.liked_news_id.append(news_id)
        news.save()
        user.save()
        data = {
            "id": news_id
        }
        return JsonResponse(data)


def change_category(request):
    if request.method == 'GET':
        category_id = request.GET.get('id', '0')
        active_categories = request.session.setdefault('active_categories', [])

        if category_id == '0':
            active_categories = []
        elif int(category_id) not in active_categories:
            active_categories.append(int(category_id))
        else:
            active_categories.remove(int(category_id))
        request.session['active_categories'] = active_categories
        data = {
            'active_categories': active_categories
        }
        current_list_view = All_News_View(request=request)
        current_list_view.reload_queryset()
        return JsonResponse(data)


def change_star(request):
    if request.method == 'GET':
        category_id = request.GET['id']
        star_category_id = request.user.star_categories_id

        if int(category_id) not in star_category_id:
            star_category_id.append(int(category_id))
        else:
            star_category_id.remove(int(category_id))
        request.user.star_categories_id = star_category_id
        request.user.save()
        data = {
            'star_category_id': star_category_id
        }
        return JsonResponse(data)

def parsing_genshin(request):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    browser = webdriver.Chrome()
    browser.get('https://genshin.hoyoverse.com/ru/news')
    print('in site')

    blocks = browser.find_elements(By.CLASS_NAME, 'news__item')
    print('got blocks')

    category = Category.objects.get(pk=1)
    print('got category')
    print(blocks)

    for news in blocks:
        print('in news')
        url = news.find_element(By.TAG_NAME, 'a').get_attribute('href')
        news_info = news.find_element(By.CLASS_NAME, 'news__info')
        name = news_info.find_element(By.TAG_NAME, 'h3').get_attribute('innerHTML')
        description = news_info.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML')

        image_url = news.find_element(By.TAG_NAME,'img').get_attribute('src')
        image_bytes = requests.get(image_url).content
        next_id = 1 if not News.objects.last() else News.objects.last().id + 1
        image_name = f'{next_id}.jpg'
        image_file = ContentFile(image_bytes, name=image_name)
        saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

        result_news = News(
            name=name,
            description=description,
            url=url,
            category=category,
            image=saved_image_path
        )
        result_news.save()
        print('saved')
    # name = browser.find_element('xpath', '/html/body/div[1]/div/div/div[3]/div/div[2]/ul[3]/li[1]/a/div/h3').get_attribute('innerHTML')
    # description = browser.find_element('xpath', '/html/body/div[1]/div/div/div[3]/div/div[2]/ul[3]/li[1]/a/div/p').get_attribute('innerHTML')
    # url = browser.find_element('xpath', '/html/body/div[1]/div/div/div[3]/div/div[2]/ul[3]/li[1]/a').get_attribute('href')
    #
    # image_url = browser.find_element('xpath', '/html/body/div[1]/div/div/div[3]/div/div[2]/ul[3]/li[1]/a/img').get_attribute('src')
    # image_bytes = requests.get(image_url).content
    # next_id = News.objects.last().id+1
    # image_name = f'{next_id}.jpg'
    # image_file = ContentFile(image_bytes, name=image_name)
    # saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

    return HttpResponseRedirect(reverse('all_news'))

def clear_hearts_from_users_and_news(request):
    for user in User.objects.all():
        user.liked_news_id.clear()
        user.save()
    for news in News.objects.all():
        news.likes = 0
        news.save()
    return HttpResponseRedirect(reverse('all_news'))

def is_malicious_code(comment):
    # Простой пример регулярного выражения для поиска скриптов
    pattern = r'<script.*?>.*?</script>|<.*?javascript:.*?>'
    if re.search(pattern, comment, re.IGNORECASE):
        return True
    return False
def leave_comment(request):
    if request.method == "GET":
        print('in get')
        comment_text = request.GET.get('text', '')
        news_id = int(request.GET['id'][14:])
        if comment_text == '':
            print('in if')
            return JsonResponse({'text': ''})
        else:
            print('in else')
            if is_malicious_code(comment_text):
                print('in else if')
                return JsonResponse({'status': 'error', 'message': 'Вредоносный код обнаружен!'})
            else:
                print('in else else')
                user = request.user
                news = News.objects.get(pk=news_id)
                comment = Comment(
                    text=comment_text,
                    user=user,
                    news=news
                )
                comment.save()
                news.comments_count += 1
                news.save()
                data = {
                    'status_code': '201'
                }
                return JsonResponse(data)

def rate_comment(request):
    if request.method == 'GET':
        user = request.user

        comment_id = int(request.GET['id'])
        click_type = request.GET['type']
        comment = Comment.objects.get(pk=comment_id)
        print('got preference')
        if click_type == 'like':
            if comment_id in user.liked_comments_id:
                print('in if')
                comment.likes -= 1
                user.liked_comments_id.remove(comment_id)
            else:
                print('in else')
                comment.likes += 1
                user.liked_comments_id.append(comment_id)
        else:
            if comment_id in user.disliked_comments_id:
                print('in if')
                comment.dislikes -= 1
                user.disliked_comments_id.remove(comment_id)
            else:
                print('in else')
                comment.dislikes += 1
                user.disliked_comments_id.append(comment_id)
        comment.save()
        user.save()
        data = {
            "id": comment_id
        }
        return JsonResponse(data)

