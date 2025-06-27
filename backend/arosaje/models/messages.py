from django.contrib.auth.models import User
from django.db import models
from .conversations import Conversations

class Messages(models.Model):
    message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    picture = models.ImageField()
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
