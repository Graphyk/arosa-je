from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

from .plants import Plants

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
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_of_event__gt=models.F('start_of_event')),
                name='start_before_end'
            ),
        ]
