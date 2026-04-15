from django.core.management.base import BaseCommand
import json
from rating.models import Service, UDR
from rating.rating_engine import rate_udr

class Command(BaseCommand):
    help = 'Ingest UDRs in batch from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file with UDRs.')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as f:
            data = json.load(f)
            for udr_json in data:
                service_id = udr_json.get('service_id')
                if not service_id:
                    self.stdout.write(self.style.ERROR('UDR missing service_id'))
                    continue
                try:
                    service = Service.objects.get(service_id=service_id)
                except Service.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Service {service_id} not found'))
                    continue
                udr = UDR.objects.create(
                    raw=udr_json,
                    timestamp=udr_json.get('timestamp'),
                    service=service,
                    usage_class=udr_json.get('usage_class'),
                    usage_amount=udr_json.get('usage_amount'),
                )
                rate_udr(udr)
                self.stdout.write(self.style.SUCCESS(f'Ingested UDR id: {udr.id}'))
