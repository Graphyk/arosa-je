from django.db import models

class Consentments(models.Model):
    name = models.CharField(max_length=64)
    required = models.BooleanField(default=False)
    text = models.TextField()
