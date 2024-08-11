from django.db import models
from users.models import User

class Donate(models.Model):
    price = models.PositiveIntegerField(default=50)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

