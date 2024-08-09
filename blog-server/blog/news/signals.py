from django.db.models.signals import post_delete
from django.dispatch import receiver
from news.models import News, Comment
from users.models import User

@receiver(post_delete, sender=News)
def post_delete_news(sender, instance, **kwargs):
    print('in post_delete')
    users = User.objects.all()
    news_id = instance.id
    comments = Comment.objects.filter(news=instance)
    news_tags = instance.tags
    for user in users:
        user.liked_news_id.remove(news_id)
        user.viewed_news_id.remove(news_id)
        for comment in comments:
            user.liked_comments_id.remove(comment.id)
            user.disliked_comments_id.remove(comment.id)
        for tag in news_tags:
            if tag in user.recommended_tags:
                if user.recommended_tags[tag] == 1:
                    user.recommended_tags.pop(tag)
                else:
                    user.recommended_tags[tag] -= 1
        user.save()
        print('saved')

@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    users = User.objects.all()
    comment_id = instance.id
    for user in users:
        user.liked_comments_id.remove(comment_id)
        user.disliked_comments_id.remove(comment_id)
        user.save()


