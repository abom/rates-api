from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()


class ExchangeRateSerializer(serializers.Serializer):
    from_currency = serializers.CharField(required=True, allow_blank=False, max_length=5)
    to_currency = serializers.CharField(required=True, allow_blank=False, max_length=5)
    rate = serializers.CharField(required=True, allow_blank=False, max_length=30)
    last_update = TimestampField()

    def to_json(self):
        return JSONRenderer().render(self.data)
