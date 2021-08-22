class Client:
    def __init__(self, provider):
        self.provider = provider

    def get(self, from_currency, to_currency):
        return self.provider.get(from_currency, to_currency)
