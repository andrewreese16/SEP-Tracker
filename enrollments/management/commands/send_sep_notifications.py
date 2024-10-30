from django.core.management.base import BaseCommand
from django.utils import timezone
from enrollments.models import Customer
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send SEP end date notifications'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Check for customers with SEP ending in 10 days
        ten_day_notifications = Customer.objects.filter(
            sep_end_date=today + timedelta(days=10),
            notification_10_days_sent=False
        )
        
        for customer in ten_day_notifications:
            customer.send_notification_email(10)
            customer.notification_10_days_sent = True
            customer.save()
        
        # Check for customers with SEP ending in 5 days
        five_day_notifications = Customer.objects.filter(
            sep_end_date=today + timedelta(days=5),
            notification_5_days_sent=False
        )
        
        for customer in five_day_notifications:
            customer.send_notification_email(5)
            customer.notification_5_days_sent = True
            customer.save()