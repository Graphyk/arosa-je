from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .posts import Posts

class Keeping(models.Model):
    STATUSES = [
        (0, "pending"),
        (1, "canceled"),
        (2, "not taken"),
        (3, "ongoing"),
        (4, "validated"),
        (5, "not gave back")
    ]

    pk = models.CompositePrimaryKey("keeper_id", "post_id")
    keeper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keeping_keeper")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    _status = models.SmallIntegerField(choices=STATUSES, default=0)

    @property
    def status(self):
        return self._status

    def clean(self):
        super().clean()

        if (self.post.start_of_event <= datetime.now().date()):
            if not Keeping.objects.filter(post_id=self.post, keeper_id=self.keeper).first():
                raise ValidationError(
                    "you can't accept a keeping at the last moment"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def cancel(self):
        if self.status != 0:
            raise ValidationError("Keeping must be pending in view to be canceled")
        self._status = 1
        self.save()

    def take(self):
        if self.status != 0:
            raise ValidationError("Keeping must be pending in view to be taken")
        self._status = 3
        self.save()

    def validate(self):
        if self.status != 3:
            raise ValidationError("Keeping must be ongoing in view to be validated")
        self._status = 4
        self.save()
