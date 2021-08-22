from dataclasses import dataclass


@dataclass
class Rate:
    from_currency: str
    to_currency: str
    rate: str
    last_update: float


class FetchError(Exception):
    pass


class Provider:
    def __init__(self, options):
        self.options = options

    def get(self, from_currency, to_currency) -> Rate:
        raise NotImplementedError

