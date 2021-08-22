from dataclasses import dataclass
import pytz
import requests

from dataclasses import dataclass
from datetime import datetime, time
from urllib.parse import urlencode

from . import FetchError, Provider, Rate


BASE_URL = "https://www.alphavantage.co/query?"
FUNCTION = "CURRENCY_EXCHANGE_RATE"


@dataclass
class ExchangeRate(Rate):
    error: str
    timezone: str

    @classmethod
    def from_json(cls, data: dict):
        # convert alphavantage response to ExchangeRate with extra error and timezone fields
        rate_data = data.get("Realtime Currency Exchange Rate", {})
        error = data.get("Error Message", "")
        timezone = rate_data.get("7. Time Zone", "utc")
        last_update = rate_data.get("6. Last Refreshed", "")
        if last_update:
            # convert to timestamp
            dt = datetime.fromisoformat(last_update)
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt)
            # always utc
            last_update = datetime.timestamp(dt.astimezone(pytz.UTC))

        return cls(
            from_currency=rate_data.get("1. From_Currency Code", ""),
            to_currency=rate_data.get("3. To_Currency Code", ""),
            rate=rate_data.get("5. Exchange Rate", ""),
            last_update=last_update,
            timezone=timezone,
            error=error,
        )


class Alphavantage(Provider):
    def get(self, from_currency, to_currency) -> Rate:
        try:
            query_params = urlencode(
                {
                    "function": FUNCTION,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "apikey": self.options.get("api_key", ""),
                }
            )

            url = f"{BASE_URL}{query_params}"
            res = requests.get(url)
            res.raise_for_status()
            rate = ExchangeRate.from_json(res.json())
            if rate.error:
                raise FetchError(rate.error)
            return rate
        except requests.HTTPError as e:
            raise FetchError(f"cannot fetch exchange rate of {from_currency}/{to_currency}: {e}") from e
