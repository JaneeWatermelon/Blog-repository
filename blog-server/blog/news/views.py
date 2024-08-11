import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common.views import TitleMixin
from news.models import Category, Comment, News
from users.models import User

import difflib
from rutermextract import TermExtractor

from functools import wraps
from django.core.exceptions import PermissionDenied

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            print('not auth')
            raise PermissionDenied
        print('yes auth')
        return view(request, *args, **kwargs)
    return wrapper

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
        print(active_categories)
        if active_categories:
            for category_id in active_categories:
                result = result.union(queryset.filter(category=Category.objects.get(pk=category_id)))
            return result.order_by('-id')
        else:
            return queryset.order_by('-id')
    def reload_queryset(self):
        self.object_list = self.get_queryset()

class Recommended_News_View(TitleMixin, ListView):
    template_name = "news/recommendations.html"
    title = 'Recommended News'
    model = News
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        result = queryset.filter(pk=0)

        if user.is_authenticated:
            sorted_user_tags = {k: v for k, v in sorted(user.recommended_tags.items(), key=lambda item: item[1], reverse=True)}
            random_news = News.objects.all().order_by('?')

            for news in random_news:
                for news_tag in news.tags:
                    for user_tag in list(sorted_user_tags.keys())[:10]:
                        matcher_result = difflib.SequenceMatcher(isjunk=None, a=user_tag, b=news_tag, autojunk=True).quick_ratio()
                        if matcher_result >= 0.7:
                            result = result.union(News.objects.filter(pk=news.id))
                            break
        return result

class Popular_News_View(TitleMixin, ListView):
    template_name = "news/popular.html"
    title = 'Popular News'
    model = News
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.all()
        result = sorted(result, key=lambda p: p.get_popularity(), reverse=True)
        return result

class New_News_View(TitleMixin, ListView):
    template_name = "news/new.html"
    title = 'New News'
    model = News
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-time')
class Full_Card_View(TitleMixin, DetailView):
    model = News
    title = 'Detail News'
    template_name = 'news/full_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(news=self.object).order_by('-time')
        return context

@ajax_login_required
def heart_news(request):

    if request.method == 'GET':
        user = request.user
        print(user.recommended_tags)

        news_id = int(request.GET['id'][5:])
        news = News.objects.get(pk=news_id)
        print('got preference')

        if news_id in user.liked_news_id:
            print('in if')
            for tag in news.tags:
                if tag in user.recommended_tags:
                    if user.recommended_tags[tag] == 1:
                        user.recommended_tags.pop(tag)
                    else:
                        user.recommended_tags[tag] -= 1
            news.likes -= 1
            user.liked_news_id.remove(news_id)
        else:
            print('in else')
            for tag in news.tags:
                if tag in user.recommended_tags:
                    user.recommended_tags[tag] += 1
                else:
                    user.recommended_tags[tag] = 1
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
        category_id = request.GET['id']
        active_categories = request.session['active_categories']

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
@ajax_login_required
def change_star(request):
    if request.method == 'GET' and request.user.is_authenticated:
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
    else:
        return HttpResponse('', status=401)
def try_get_key_words(title, description):
    term_extractor = TermExtractor()
    text = title + ' ' + description
    result_list = []
    for term in term_extractor(text, nested=True):
        result_list.append(term.normalized)
    return result_list
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
        if not News.objects.filter(url=url):
            news_info = news.find_element(By.CLASS_NAME, 'news__info')
            name = news_info.find_element(By.TAG_NAME, 'h3').get_attribute('innerHTML')
            description = news_info.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML')

            image_url = news.find_element(By.TAG_NAME,'img').get_attribute('src')
            image_bytes = requests.get(image_url).content
            next_id = 1 if not News.objects.last() else News.objects.last().id + 1
            image_name = f'{next_id}.jpg'
            image_file = ContentFile(image_bytes, name=image_name)
            saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)
            tags = (try_get_key_words(name, description)[:10])

            result_news = News(
                name=name,
                description=description,
                url=url,
                category=category,
                image=saved_image_path,
                tags=tags
            )
            result_news.save()
            print('saved')
        else:
            break
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

@ajax_login_required
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

@ajax_login_required
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
                if comment_id in user.disliked_comments_id:
                    comment.dislikes -= 1
                    user.disliked_comments_id.remove(comment_id)
                comment.likes += 1
                user.liked_comments_id.append(comment_id)
        else:
            if comment_id in user.disliked_comments_id:
                print('in if')
                comment.dislikes -= 1
                user.disliked_comments_id.remove(comment_id)
            else:
                print('in else')
                if comment_id in user.liked_comments_id:
                    comment.likes -= 1
                    user.liked_comments_id.remove(comment_id)
                comment.dislikes += 1
                user.disliked_comments_id.append(comment_id)
        comment.save()
        user.save()
        data = {
            "id": comment_id
        }
        return JsonResponse(data)

def check_view(request):
    if request.method == "GET":
        news_id = int(request.GET['id'])
        user = request.user

        if news_id not in user.viewed_news_id:
            user.viewed_news_id.append(news_id)
            user.save()
        news = News.objects.get(pk=news_id)
        news.views += 1
        print('+1')
        news.save()

        return JsonResponse({})


