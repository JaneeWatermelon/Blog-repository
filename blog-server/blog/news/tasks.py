from celery import shared_task

from news.models import Category, News, AllNewsURLs
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rutermextract import TermExtractor
import redis
from django.utils.timezone import timedelta, now

# import os
# from PIL import Image
# from django.conf import settings

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def is_running(task_name):
    if redis_client.get(task_name):
        return True
    return False

def set_running(task_name):
    redis_client.set(task_name, 'true', ex=3600)

def clear_running(task_name):
    redis_client.delete(task_name)

def delete_old_news():
    now_time = now()
    for news in News.objects.all().order_by('time'):
        if news.time + timedelta(days=14) < now_time:
            news.delete()
        else:
            break

def try_get_key_words(title, description):
    term_extractor = TermExtractor()
    text = f'{title} {description}'
    result_list = []
    for term in term_extractor(text, nested=True):
        result_list.append(term.normalized)
    return result_list
def parsing_playground(adds_url, category_id):
    # every 1 hour i think
    category = Category.objects.get(pk=category_id)

    response = requests.get(f'https://www.playground.ru/news/{adds_url}')

    soup = BeautifulSoup(response.text, 'lxml')

    news_block = soup.find('div', id='postListContainer')
    all_news = news_block.find_all('div', class_='post')[::-1]

    all_news_urls = AllNewsURLs.objects.first()

    for news in all_news:
        try:
            post_title_a = news.find('div', class_='post-title').find('a')
            news_link = post_title_a['href']
            name = post_title_a.text.strip()
        except Exception:
            continue
        if news_link not in all_news_urls.urls:
            full_news = requests.get(news_link)
            full_soup = BeautifulSoup(full_news.text, 'lxml')

            article_content = full_soup.find('div', class_='article-content')
            try:
                image_url = article_content.find('img')['src']
            except Exception:
                image_url = news.find('img')['src']
            image_bytes = requests.get(image_url).content
            next_id = 1 if not News.objects.last() else News.objects.last().id + 1
            image_name = f'{next_id}.webp'
            image_file = ContentFile(image_bytes, name=image_name)
            saved_image_path = default_storage.save(f'news_images/{category.name}/{image_name}', image_file)


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
            all_news_urls.urls += [news_link]
            all_news_urls.save()
            print('saved')

@shared_task
def call_playground():
    task_name = 'call_playground'
    if is_running(task_name):
        return 'Task is already running'
    set_running(task_name)

    adds_url = ['movies', 'hardware', 'pc', 'industry', 'consoles']
    for i in range(1, 6):
        if i >= 3:
            parsing_playground(adds_url[i - 1], 3)
        else:
            parsing_playground(adds_url[i - 1], i)
    clear_running(task_name)

def parsing_womanhit(adds_url, category_id):
    # every day i think
    domain_url = 'https://www.womanhit.ru'

    link = f'{domain_url}{adds_url}'

    category = Category.objects.get(pk=category_id)
    response = requests.get(link)

    soup = BeautifulSoup(response.text, 'lxml')

    all_news = soup.find_all('article', class_='card')[::-1]

    all_news_urls = AllNewsURLs.objects.first()
    for news in all_news:
        try:
            news_link = f"{domain_url}{news.find('a')['href']}"
        except Exception:
            continue
        if news_link not in all_news_urls.urls:
            full_news = requests.get(news_link)
            full_soup = BeautifulSoup(full_news.text, 'lxml')

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
            all_news_urls.urls += [news_link]
            all_news_urls.save()
            print('saved')

@shared_task
def call_womanhit():
    task_name = 'call_womanhit'
    if is_running(task_name):
        return 'Task is already running'
    set_running(task_name)
    delete_old_news()
    adds_url = [
        '/lifestyle/fashion/',
        '/at-home/food/',
        '/at-home/interier/',
        '/at-home/dacha/',
        '/health-and-beauty/',
    ]
    for i in range(4, 9):
        parsing_womanhit(adds_url[i-4], i)
    clear_running(task_name)

# @shared_task
# def change_images():
#     news_items = News.objects.all()
#     for item in news_items:
#         if item.image:
#             image_path = os.path.join(settings.MEDIA_ROOT, item.image.name)
#             image = Image.open(image_path)
#             webp_image_path = image_path.replace('.jpg', '.webp')
#
#             image.save(webp_image_path, 'webp')
#
#             # Обновите путь к изображению в базе данных
#             item.image.name = item.image.name.replace('.jpg', '.webp')
#             item.save()
#
#             # Удалите старый файл
#             os.remove(image_path)
#     print('Замена изображений завершена')

