from django.db import models
from address.models import AddressField

from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length=64)
    water_dependency = models.IntegerField()
    light_dependency = models.IntegerField()
    creation_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

class Plants(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField()
    address = AddressField(related_name='+', blank=True, null=True)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

class Commentaries(models.Model):
    commentary = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)

class Posts(models.Model):
    commentary = models.TextField()
    start_of_event = models.DateTimeField()
    end_of_event = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)

class Keeping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keeping_user")
    keeper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keeping_keeper")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Conversations(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_user_2")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Messages(models.Model):
    message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    picture = models.ImageField()
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
