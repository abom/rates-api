from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from rateapi.app.models import APIKey


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("key", type=str)

    def handle(self, *args, **options):
        key = options["key"]
        try:
            api_key = APIKey.objects.get(key=key)
            api_key.delete()
            self.stdout.write(self.style.SUCCESS(f"API key of {key} is now revoked"))
        except ObjectDoesNotExist:
            raise CommandError(f"API key of {key} does not exist")

