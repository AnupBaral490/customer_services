from django.db import models
import re


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    suburb = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.full_name

    def format_phone(self):
        """Format Australian phone number for display."""
        phone = self.phone.replace(' ', '').replace('-', '')
        if phone.startswith('04') or phone.startswith('02') or phone.startswith('07'):
            return f"{phone[:2]} {phone[2:6]} {phone[6:]}"
        return phone
