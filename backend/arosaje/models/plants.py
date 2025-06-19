from address.models import AddressField
from django.contrib.auth.models import User
from django.db import models

import uuid
import os

from .species import Species

def plant_picture_upload_to(instance, filename):
    # Récupère l'extension du fichier original
    ext = filename.split('.')[-1]
    # Crée un nom unique (par exemple avec l'id du propriétaire et un UUID)
    filename = f"{instance.owner.id}_{uuid.uuid4()}.{ext}"
    # Place le fichier dans un dossier par espèce
    return os.path.join('plants', filename)

class Plants(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=plant_picture_upload_to)
    address = AddressField(related_name='+', blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)
