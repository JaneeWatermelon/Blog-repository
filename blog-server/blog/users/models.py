from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    liked_news_id = models.JSONField(blank=True, null=True)
    viewed_news_id = models.JSONField(blank=True, null=True)
    star_categories_id = models.JSONField(blank=True, null=True)
