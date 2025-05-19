from address.models import AddressField
from django.contrib.auth.models import User
from django.db import models

from .species import Species


class Plants(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField()
    address = AddressField(related_name='+', blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)
