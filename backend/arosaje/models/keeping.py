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
            raise ValidationError(
                "you can't accept a keeping at the last moment"
            )
