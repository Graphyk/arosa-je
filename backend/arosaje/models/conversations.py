from django.contrib.auth.models import User
from django.db import models

from .posts import Posts

class Conversations(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_2")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
