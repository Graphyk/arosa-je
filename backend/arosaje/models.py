from django.db import models
from address.models import AddressField

from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    start_of_event = models.DateField()
    end_of_event = models.DateField()
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        #modify to a SQL constraint when migrating to postgres
        if self.start_of_event <= datetime.now().date():
            raise ValidationError(
                "starting date of a post must be superior to today's date."
            )

        post_from_plant = Posts.objects.filter(plant=self.plant)
        overlap = post_from_plant.filter(
            start_of_event__lte=self.end_of_event,
            end_of_event__gte=self.end_of_event
        ) | post_from_plant.filter(
            start_of_event__lte=self.start_of_event,
            end_of_event__gte=self.start_of_event
        ) | post_from_plant.filter(
            start_of_event__gte=self.start_of_event,
            end_of_event__lte=self.end_of_event
        )
        
        if self.pk:
            overlap = overlap.exclude(pk=self.pk)
        
        if overlap.exists():
            raise ValidationError(
                "There is already a period for this plant that overlap specified dates."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Assure que la validation est toujours exécutée
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_of_event__gt=models.F('start_of_event')),
                name='start_before_end'
            ),
        ]

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
