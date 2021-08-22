import json

from django.core.cache import cache


KEY = "rate.current"


def set(rate):
    cache.set(KEY, json.dumps(rate))


def get():
    data = cache.get(KEY)
    if data:
        return json.loads(data)
    return data


def invalidate():
    cache.delete(KEY)
