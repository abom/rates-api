import random
import string

from django.core.management.base import BaseCommand, CommandError

from rateapi.app.models import APIKey


KEY_LEN = 64


class Command(BaseCommand):
    help = "Generate API keys"

    def handle(self, *args, **options):
        random_key = "".join(random.choices(string.ascii_letters + string.digits, k=64))
        api_key, created = APIKey.objects.get_or_create(key=random_key)
        if created:
            api_key.save()

        self.stdout.write(self.style.SUCCESS(f"Generated API key: {random_key}"))
