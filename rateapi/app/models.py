from django.db import models
from django.db.models import indexes


class ExchangeRate(models.Model):
    from_currency = models.CharField(max_length=5)
    to_currency = models.CharField(max_length=5)
    rate = models.CharField(max_length=30)
    last_update = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["last_update"])]


class APIKey(models.Model):
    key = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["key"])]
