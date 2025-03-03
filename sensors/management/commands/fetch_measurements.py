
from django.core.management.base import BaseCommand
from sensors.services import FetchOpenAQMeasurements

class Command(BaseCommand):
    help = "Fetches latest measurements from OpenAQ API"

    def handle(self, *args, **kwargs):
        FetchOpenAQMeasurements.fetch_latest_measurements()
        self.stdout.write("All measurements fetched successfully")
