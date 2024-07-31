from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, default='profilo.jpg')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    liked_news_id = models.JSONField(default=list)
    viewed_news_id = models.JSONField(default=list)
    star_categories_id = models.JSONField(default=list)
