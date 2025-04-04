from django.db import models

class Species(models.Model):
    name = models.CharField(max_length=64)
    water_dependency = models.IntegerField()
    light_dependency = models.IntegerField()
    creation_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)
