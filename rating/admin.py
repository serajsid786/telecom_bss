from django.contrib import admin
from .models import Customer, Service, UDR, RatePlan, RateRule, Tax, Promotion, Invoice, UUIH

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(UDR)
admin.site.register(RatePlan)
admin.site.register(RateRule)
admin.site.register(Tax)
admin.site.register(Promotion)
admin.site.register(Invoice)
admin.site.register(UUIH)