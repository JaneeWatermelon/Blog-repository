from celery import shared_task
from users.models import User, EmailVerification

from django.utils.timezone import now, timedelta
import uuid

import logging

logger = logging.getLogger(__name__)

from news.models import Category, Comment, News
import fake_useragent
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from news.views import try_get_key_words

@shared_task
def send_email_task(user_id):
    print('in task')
    user = User.objects.get(pk=user_id)
    expiration = now() + timedelta(hours=24)
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=user,
        expiration=expiration
    )
    record.send_verification_email()

@shared_task
def parsing_playground_games():
    # every 1 hour i think
    game_urls = ['pc', 'industry', 'consoles']
    category = Category.objects.get(pk=3)
    for i in range(1):
        response = requests.get(f'https://www.playground.ru/news/{game_urls[i]}')

        soup = BeautifulSoup(response.text, 'lxml')

        news_block = soup.find('div', id='postListContainer')
        all_news = news_block.find_all('div', class_='post')[:5]

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