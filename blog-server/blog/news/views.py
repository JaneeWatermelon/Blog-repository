import datetime
from difflib import SequenceMatcher
import re, os
import time
from functools import wraps, lru_cache
from django.utils.timezone import now, timedelta
from PIL import Image
from django.conf import settings

import fake_useragent
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rutermextract import TermExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By

from common.views import TitleMixin
from news.models import Category, Comment, News
from users.models import User
from django.core.paginator import Paginator
# from news.tasks import change_images

per_page = 24


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper

class All_News_View(TitleMixin, ListView):
    template_name = "news/all_news.html"
    title = 'Новости из разных категорий Blogus'
    model = News
    paginate_by = per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        active_categories = self.request.session.setdefault('active_categories', [])
        if active_categories:
            categories_ids = []
            for category_id in active_categories:
                categories_ids.append(category_id)
            news_categories = Category.objects.filter(pk__in=categories_ids)
            return queryset.filter(category__in=news_categories).order_by('-id')
        else:
            return queryset.order_by('-id')
    def reload_queryset(self):
        self.object_list = self.get_queryset()

class Recommended_News_View(TitleMixin, ListView):
    template_name = "news/recommendations.html"
    title = 'Рекомендованные новости для вас! Blogus'
    model = News
    paginate_by = per_page

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            sorted_user_tags = {k: v for k, v in sorted(user.recommended_tags.items(), key=lambda item: item[1], reverse=True)}
            user_tags = list(sorted_user_tags.keys())[:15]

            if user_tags:
                result = self.get_recommended_news(user_tags)
            else:
                result = queryset.none()

            return result

        return queryset.none()

    def get_recommended_news(self, user_tags):
        all_news = News.objects.all()

        @lru_cache(maxsize=1024)
        def get_matcher_result(tag1, tag2):
            return SequenceMatcher(None, tag1, tag2).quick_ratio()

        news_ids = []

        for news in all_news:
            is_break = False
            news_id = news.id
            matches = 0

            for user_tag in user_tags:
                for news_tag in news.tags:
                    matcher_result = get_matcher_result(user_tag, news_tag)

                    if matcher_result >= 0.7:
                        matches += 1

                        if matches >= 2:
                            news_ids.append(news_id)
                            is_break = True
                            break
                if is_break:
                    break
        result = all_news.filter(pk__in=news_ids)
        return result

class Popular_News_View(TitleMixin, ListView):
    template_name = "news/popular.html"
    title = 'Самые популярные новости Blogus'
    model = News
    paginate_by = per_page
    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset
        result = sorted(result, key=lambda p: p.get_popularity(), reverse=True)
        return result

class New_News_View(TitleMixin, ListView):
    template_name = "news/new.html"
    title = 'Свежие новости за последний день Blogus'
    model = News
    paginate_by = per_page
    def get_queryset(self):
        queryset = super().get_queryset()

        time_ago = now() - timedelta(hours=24)
        # Создаем список, чтобы хранить подходящие новости
        news_ids = []
        # Итерируемся по новостям
        for news in queryset.order_by('-id'):
            if news.time >= time_ago:
                news_ids.append(news.id)  # добавляем id в список
            else:
                break  # если попалось время меньше, можно остановиться
        # Получаем итоговый queryset из ids
        result = News.objects.filter(pk__in=news_ids).order_by('-id')
        return result
class Full_Card_View(DetailView):
    model = News
    template_name = 'news/full_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(news=self.object).order_by('-time')
        context['title'] = self.object.name
        return context

def all_paginator(request):
    queryset = All_News_View(request=request).get_queryset()
    paginate_by = per_page
    paginator = Paginator(queryset, paginate_by)
    return paginator

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
        prev_page_number = int(request.GET.get('page', 1000))
        category_id = request.GET['id']
        active_categories = request.session['active_categories']

        if category_id == '0':
            active_categories = []
        elif int(category_id) not in active_categories:
            active_categories.append(int(category_id))
        else:
            active_categories.remove(int(category_id))
        request.session['active_categories'] = active_categories
        current_list_view = All_News_View(request=request)
        current_list_view.reload_queryset()
        print('changed')
        data = {'redirect': False, 'choosed_theme': request.session['choosed_theme']}
        if all_paginator(request).num_pages < prev_page_number:
            print('in if after change')
            data['redirect'] = True
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

        if user.is_authenticated and news_id not in user.viewed_news_id:
            user.viewed_news_id.append(news_id)
            user.save()
        news = News.objects.get(pk=news_id)
        news.views += 1
        print('+1')
        news.save()

        return JsonResponse({})

def change_show_type(request):
    if request.method == "GET":
        request.session['show_type'] = request.GET['show_type']
        return JsonResponse({})

def try_get_key_words(title, description):
    term_extractor = TermExtractor()
    text = f'{title} {description}'
    result_list = []
    for term in term_extractor(text, nested=True):
        result_list.append(term.normalized)
    return result_list

def parsing_genshin(request):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    browser = webdriver.Chrome(options=option)
    browser.get('https://genshin.hoyoverse.com/ru/news')
    print('in site')

    for i in range(2):
        read_more = browser.find_element(By.CLASS_NAME, 'news__more')
        print(read_more.get_attribute('innerHTML'))
        read_more.click()
        time.sleep(3)

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

def parsing_playground_movies(request):
    # every 3 hours i think
    response = requests.get('https://www.playground.ru/news/movies')
    category = Category.objects.get(pk=1)

    soup = BeautifulSoup(response.text, 'lxml')

    news_block = soup.find('div', id='postListContainer')
    all_news = news_block.find_all('div', class_='post')[::-1]

    for news in all_news:
        news_link = news.find('div', class_='post-title').find('a')['href']
        if not News.objects.filter(url=news_link):
            full_news = requests.get(news_link)
            full_soup = BeautifulSoup(full_news.text, 'lxml')

            print(news_link)
            article_content = full_soup.find('div', class_='article-content')
            try:
                image_url = article_content.find('img')['src']
            except Exception:
                image_url = news.find('img')['src']
            image_bytes = requests.get(image_url).content
            next_id = 1 if not News.objects.last() else News.objects.last().id + 1
            image_name = f'{next_id}.jpg'
            image_file = ContentFile(image_bytes, name=image_name)
            saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

            name = full_soup.find('h1', class_='post-title').text.strip()
            description = article_content.text.strip()

            for fig in article_content.find_all('figure'):
                fig.extract()
            for pg in article_content.find_all('pg-embed'):
                pg.extract()
            description_for_html = ''.join(str(content) for content in article_content.contents if content != '\n')
            tags = (try_get_key_words(name, description)[:15])

            result_news = News(
                name=name,
                description=description,
                description_for_html=description_for_html,
                url=news_link,
                base_url='https://www.playground.ru/',
                category=category,
                image=saved_image_path,
                tags=tags
            )
            result_news.save()
            print('saved')
    return HttpResponseRedirect(reverse('all_news'))

def parsing_playground_hardware(request):
    # every 12 hours i think
    response = requests.get('https://www.playground.ru/news/hardware')
    category = Category.objects.get(pk=2)

    soup = BeautifulSoup(response.text, 'lxml')

    news_block = soup.find('div', id='postListContainer')
    all_news = news_block.find_all('div', class_='post')[::-1]

    for news in all_news:
        news_link = news.find('div', class_='post-title').find('a')['href']
        if not News.objects.filter(url=news_link):
            full_news = requests.get(news_link)
            full_soup = BeautifulSoup(full_news.text, 'lxml')

            print(news_link)
            article_content = full_soup.find('div', class_='article-content')
            try:
                image_url = article_content.find('img')['src']
            except Exception:
                image_url = news.find('img')['src']
            image_bytes = requests.get(image_url).content
            next_id = 1 if not News.objects.last() else News.objects.last().id + 1
            image_name = f'{next_id}.jpg'
            image_file = ContentFile(image_bytes, name=image_name)
            saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

            name = full_soup.find('h1', class_='post-title').text.strip()
            description = article_content.text.strip()

            for fig in article_content.find_all('figure'):
                fig.extract()
            for pg in article_content.find_all('pg-embed'):
                pg.extract()
            description_for_html = ''.join(str(content) for content in article_content.contents if content != '\n')
            tags = (try_get_key_words(name, description)[:15])

            result_news = News(
                name=name,
                description=description,
                description_for_html=description_for_html,
                url=news_link,
                base_url='https://www.playground.ru/',
                category=category,
                image=saved_image_path,
                tags=tags
            )
            result_news.save()
            print('saved')
    return HttpResponseRedirect(reverse('all_news'))

def parsing_playground_games(request):
    # every 1 hour i think
    adds_url = ['movies', 'hardware', 'pc', 'industry', 'consoles']
    for i in range(1, 6):
        game_url = adds_url[i - 1]
        if i >= 3:
            category = Category.objects.get(pk=3)
        else:
            category = Category.objects.get(pk=i)
        response = requests.get(f'https://www.playground.ru/news/{game_url}')

        soup = BeautifulSoup(response.text, 'lxml')

        news_block = soup.find('div', id='postListContainer')
        all_news = news_block.find_all('div', class_='post')[::-1]

        for news in all_news:
            news_link = news.find('div', class_='post-title').find('a')['href']
            if not News.objects.filter(url=news_link):
                full_news = requests.get(news_link)
                full_soup = BeautifulSoup(full_news.text, 'lxml')

                print(news_link)
                article_content = full_soup.find('div', class_='article-content')
                try:
                    image_url = article_content.find('img')['src']
                except Exception:
                    image_url = news.find('img')['src']
                image_bytes = requests.get(image_url).content
                next_id = 1 if not News.objects.last() else News.objects.last().id + 1
                image_name = f'{next_id}.jpg'
                image_file = ContentFile(image_bytes, name=image_name)
                saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

                name = full_soup.find('h1', class_='post-title').text.strip()
                description = article_content.text.strip()

                for fig in article_content.find_all('figure'):
                    fig.extract()
                for pg in article_content.find_all('pg-embed'):
                    pg.extract()
                description_for_html = ''.join(str(content) for content in article_content.contents if content != '\n')
                tags = (try_get_key_words(name, description)[:15])

                result_news = News(
                    name=name,
                    description=description,
                    description_for_html=description_for_html,
                    url=news_link,
                    base_url='https://www.playground.ru/',
                    category=category,
                    image=saved_image_path,
                    tags=tags
                )
                result_news.save()
                print('saved')
    return HttpResponseRedirect(reverse('all_news'))

def delete_old_news():
    now_time = now()
    for news in News.objects.all().order_by('time'):
        if news.time + timedelta(days=14) < now_time:
            news.delete()
        else:
            break

def parsing_womanhit(request):
    delete_old_news()

    # every day i think
    domain_url = 'https://www.womanhit.ru'
    # '/lifestyle/fashion/' 4
    # '/at-home/food/' 5
    # '/at-home/interier/' 6
    # '/at-home/dacha/' 7
    # '/health-and-beauty/' 8
    adds = [
        '/lifestyle/fashion/',
        '/at-home/food/',
        '/at-home/interier/',
        '/at-home/dacha/',
        '/health-and-beauty/',
    ]
    for i in range(4, 9):

        adds_url = adds[i - 4]
        category_id = i
        print(adds_url)
        print(category_id)

        link = f'{domain_url}{adds_url}'

        category = Category.objects.get(pk=category_id)
        response = requests.get(link)

        soup = BeautifulSoup(response.text, 'lxml')

        all_news = soup.find_all('article', class_='card')[::-1]

        for news in all_news:
            try:
                news_link = f"{domain_url}{news.find('a')['href']}"
                print('in try')
            except Exception:
                print('in except')
                continue
            if not News.objects.filter(url=news_link):
                full_news = requests.get(news_link)
                full_soup = BeautifulSoup(full_news.text, 'lxml')

                print(news_link)
                article_content = full_soup.find('article', class_='article')
                try:
                    image_url = f"{domain_url}{article_content.find('picture').find('img')['src']}"
                except Exception:
                    continue
                image_bytes = requests.get(image_url).content
                next_id = 1 if not News.objects.last() else News.objects.last().id + 1
                image_name = f'{next_id}.webp'
                image_file = ContentFile(image_bytes, name=image_name)
                saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)

                name = article_content.find('figcaption').find('h1').text.strip()
                desc_div = article_content.find('span', itemprop='articleBody')
                description = desc_div.text.strip()

                for div in desc_div.find_all('div'):
                    div.extract()
                description_for_html = ''.join(str(content) for content in desc_div.contents if content.text != '')
                tags_div = full_soup.find('div', class_='article__tags')
                try:
                    tags = list(span.text for span in tags_div.find_all('span'))
                except Exception:
                    tags = (try_get_key_words(name, description)[:15])

                result_news = News(
                    name=name,
                    description=description,
                    description_for_html=description_for_html,
                    url=news_link,
                    base_url='https://www.womanhit.ru/',
                    category=category,
                    image=saved_image_path,
                    tags=tags
                )
                result_news.save()
                print('saved')
    return HttpResponseRedirect(reverse('all_news'))

def fill_categories(request):
    names = ['Кино и сериалы', 'Железо', 'Игры', 'Мода', 'Еда', 'Интерьер', 'Дача', 'Красота']
    for name in names:
        category = Category.objects.create(name=name)
        category.save()
    return HttpResponseRedirect(reverse('all_news'))

def replace_all_news_images_to_webp(request):
    news_items = News.objects.all()
    for item in news_items:
        if item.image:
            image_path = os.path.join(settings.MEDIA_ROOT, item.image.name)
            image = Image.open(image_path)
            webp_image_path = image_path.replace('.jpg', '.webp')

            image.save(webp_image_path, 'webp')

            # Обновите путь к изображению в базе данных
            item.image.name = item.image.name.replace('.jpg', '.webp')
            item.save()

            # Удалите старый файл
            os.remove(image_path)
    return HttpResponseRedirect(reverse('all_news'))

def change_theme(request):
    if request.method == "GET":
        theme = request.session.setdefault('choosed_theme', 'light')
        if theme == 'light':
            request.session['choosed_theme'] = 'dark'
        else:
            request.session['choosed_theme'] = 'light'
        print('in views')
        print(request.session['choosed_theme'])
        return JsonResponse({'choosed_theme': request.session['choosed_theme']})