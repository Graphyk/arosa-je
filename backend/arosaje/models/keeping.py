from django.contrib.auth.models import User
from django.db import models

from .posts import Posts

class Keeping(models.Model):
    keeper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keeping_keeper")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
