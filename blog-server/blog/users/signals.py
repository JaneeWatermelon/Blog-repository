from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver

from news.models import Comment, News
from users.models import User


@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, **kwargs):
    for news_id in instance.liked_news_id:
        news = News.objects.get(pk=news_id)
        news.likes -= 1
        news.save()
    for news_id in instance.viewed_news_id:
        news = News.objects.get(pk=news_id)
        news.views -= 1
        news.save()
    for comment_id in instance.liked_comments_id:
        comment = Comment.objects.get(pk=comment_id)
        comment.likes -= 1
        comment.save()
    for comment_id in instance.disliked_comments_id:
        comment = Comment.objects.get(pk=comment_id)
        comment.dislikes -= 1
        comment.save()