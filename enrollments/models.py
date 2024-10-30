# enrollments/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone  # Import timezone

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    sep_start_date = models.DateField()
    sep_end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_10_days_sent = models.BooleanField(default=False)
    notification_5_days_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate SEP end date (60 days from start date)
        if self.sep_start_date:
            self.sep_end_date = self.sep_start_date + timedelta(days=60)
        super().save(*args, **kwargs)

        # Check if notifications need to be sent
        if not self.notification_10_days_sent and (self.sep_end_date - timezone.now().date()).days == 10:
            self.send_notification_email(10)
            self.notification_10_days_sent = True
        if not self.notification_5_days_sent and (self.sep_end_date - timezone.now().date()).days == 5:
            self.send_notification_email(5)
            self.notification_5_days_sent = True

    def send_notification_email(self, days_remaining):
        subject = f'SEP Ending Soon - {self.full_name}'
        message = f'''
        Customer: {self.full_name}
        SEP End Date: {self.sep_end_date}
        Days Remaining: {days_remaining}
        
        Please follow up with the customer regarding their enrollment status.
        '''
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.created_by.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.full_name
