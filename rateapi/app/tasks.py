import dramatiq

from periodiq import cron

from .helpers import fetch_and_save_rate


@dramatiq.actor(periodic=cron("* * * * *"))
def hourly():
    fetch_and_save_rate()
