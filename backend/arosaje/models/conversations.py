from django.contrib.auth.models import User
from django.db import models

from .keeping import Keeping

class Conversations(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_1")
    keeper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_2")
    keeping = models.ForeignKey(Keeping, on_delete=models.CASCADE)
