from django.db import models
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    external_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.external_id})"
    
class Service(models.Model):
    service_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='services')
    active_from = models.DateTimeField()
    active_to = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} - ({self.service_id})"
    

class UDR(models.Model):
    raw = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='udrs')
    usage_class = models.CharField(max_length=50)
    usage_amount = models.DecimalField(max_digits=18, decimal_places=6)
    rated_amount = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    currency = models.CharField(max_length=10, default='USD')
    billed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class RatePlan(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class RateRule(models.Model):
    plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name='rules')
    usage_class = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=6)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    geo = models.CharField(max_length=50, blank=True, null=True)

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    total_before_tax = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    tax_amount = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class UUIH(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='uuihs')
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(blank=True, null=True)