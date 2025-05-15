import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Case, When, Value, SmallIntegerField, Q

from arosaje.models import Keeping

class Command(BaseCommand):
    help = "Update keepings status"

    def handle(self, *args, **options):
          with transaction.atomic():
              Keeping.objects.filter(
                  _status=0, post__start_of_event__lt=datetime.datetime.now()
                ).update(
                  _status=2
                )
              Keeping.objects.filter(
                  _status=3, post__end_of_event__lt=datetime.datetime.now()
                ).update(
                  _status=5
                )