from django.contrib.auth.models import User

from django.db import models
from .consentments import Consentments

class ConsentmentAcceptances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="consentment_acceptances")
    consentment = models.ForeignKey(Consentments, on_delete=models.CASCADE, related_name="acceptances")
    accepted = models.BooleanField(default=False)
