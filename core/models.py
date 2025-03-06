from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length=64)
    water_dependency = models.IntegerField()
    light_dependency = models.IntegerField()
    creation_time = models.TimeField()
    update_time = models.TimeField()

class Plant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField()
    # adress
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    # commentaries
