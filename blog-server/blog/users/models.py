from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse, reverse_lazy

from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, default='profilo.jpg')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    liked_news_id = models.JSONField(default=list)
    viewed_news_id = models.JSONField(default=list)
    star_categories_id = models.JSONField(default=list)
    liked_comments_id = models.JSONField(default=list)
    disliked_comments_id = models.JSONField(default=list)
    recommended_tags = models.JSONField(default=dict)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse('users:verify', kwargs={'code': self.code, 'email': self.user.email})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = 'Blogus - Подтверждение почты'
        html_message = f'Чтобы подтвердить свою учётную запись перейдите по <a href="{verification_link}">ссылке</a>'
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            subject=subject,
            html_message=html_message,
            from_email=from_email,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration

