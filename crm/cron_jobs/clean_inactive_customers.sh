#!/bin/bash
cd "$(dirname "$0)/../.."

deleted_count = $(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer, Order
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.values_list('customer_id', flat=True).distinct()
).filter(order_date__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)")

current_time=$(date '+%Y-%m-%d %H:%M:%S')
echo "$current_time - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt