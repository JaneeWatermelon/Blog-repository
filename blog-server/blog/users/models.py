from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import News, Category

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    liked_news = models.ManyToManyField(to=News)
    viewed_news = models.ManyToManyField(to=News)
    star_categories = models.ManyToManyField(to=Category)
