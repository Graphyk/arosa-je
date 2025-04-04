from django.contrib.auth.models import User
from django.db import models

from .plants import Plants

class Commentaries(models.Model):
    commentary = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
