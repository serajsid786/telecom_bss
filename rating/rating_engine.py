from decimal import Decimal
from .models import RateRule, Promotion, Tax, UDR
from django.utils import timezone
    
def find_rate_rule(udr):
    rules = RateRule.objects.filter(usage_class=udr.usage_class)
    if not rules.exists():
        return None
    return rules.first()

def rate_udr(udr: UDR):
    rule = find_rate_rule(udr)
    if not rule:
        udr.rated_amount = Decimal('0')
        udr.save()
        return udr

    # --- Base logic ---
    base = Decimal(str(udr.usage_amount)) * rule.price_per_unit
    
    # --- Promotion logic ---
    promo_discount = Decimal('0')
    now = timezone.now()
    promos = Promotion.objects.filter(valid_from__lte=now, valid_to__gte=now)
    if promos.exists():
        promo = promos.first()
        promo_discount = (base * promo.discount_percent) / Decimal('100')
    
    # --- Tax Logic ---
    taxed = base - promo_discount
    tax_total = Decimal('0')
    for t in Tax.objects.all():
        tax_total += (taxed * t.percentage) / Decimal('100') 

    # --- Final amount ---
    final = taxed + tax_total

    udr.rated_amount = final.quantize(Decimal('0.000001'))
    udr.save()
    return udr