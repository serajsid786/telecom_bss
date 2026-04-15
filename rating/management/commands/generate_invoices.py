from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum
from rating.models import Customer, UDR, Invoice


class Command(BaseCommand):
    help = 'Generate invoices for all customers.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        period_end = now

        customers = Customer.objects.all()
        for customer in customers:
            udrs = UDR.objects.filter(service__customer=customer, billed=False)
            total_before_tax = udrs.aggregate(Sum('rated_amount'))['rated_amount__sum'] or 0
            tax_amount = total_before_tax * Decimal('0.1')  # Assume fixed 10% tax rate here for demo
            total = total_before_tax + tax_amount

            invoice = Invoice.objects.create(
                customer=customer,
                period_start=period_start,
                period_end=period_end,
                total_before_tax=total_before_tax,
                tax_amount=tax_amount,
                total=total
            )

            udrs.update(billed=True)

            self.stdout.write(self.style.SUCCESS(
                f'Generated invoice {invoice.id} for customer {customer.external_id}'
            ))
