from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField(max_length=1000)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class News(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news_images', blank=True, null=True)
    url = models.URLField()
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    comments = models.ManyToManyField(to=Comment, blank=True)
    tags = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
