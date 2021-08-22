import os
import pytz

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from rates import Client
from rates.providers import FetchError
from rates.providers.alphavantage import Alphavantage

from rateapi.app import rate_cache
from rateapi.app.models import APIKey, ExchangeRate
from rateapi.app.serializer import ExchangeRateSerializer
from rateapi.logger import logger

# should be configurable
FROM_TO = ("btc", "usd")


class NoRatesError(Exception):
    pass


def fetch_and_save_rate():
    provider = Alphavantage({"api_key": os.environ.get("ALPHAVANTAGE_API_KEY", "")})
    client = Client(provider)
    try:
        rate = client.get(*FROM_TO)
        record, created = ExchangeRate.objects.get_or_create(
            from_currency=rate.from_currency,
            to_currency=rate.to_currency,
            rate=rate.rate,
            last_update=datetime.fromtimestamp(rate.last_update).astimezone(pytz.UTC),
        )

        if created:
            record.save()
            rate_cache.invalidate()
            logger.info("created a new rate record")
        else:
            logger.info("didn't create a new rate record, no updates")

    except FetchError:
        logger.exception("error while fetching rates")
        raise


def get_current_rate():
    cached = rate_cache.get()
    if not cached:
        result = ExchangeRate.objects.order_by("last_update")
        if not result.exists():
            raise NoRatesError("no exchange rates have been fetched yet")

        object = result.last()
        serialized = ExchangeRateSerializer(object)
        cached = serialized.data
        rate_cache.set(cached)
    return cached


def is_authenticated(key):
    try:
        APIKey.objects.get(key=key)
        return True
    except ObjectDoesNotExist:
        return False
