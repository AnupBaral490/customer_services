from django.db import models
from django.contrib.auth.models import User
import re


class CustomerProfile(models.Model):
    """Customer profile linked to Django's default User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    suburb = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    last_login_notified = models.BooleanField(default=False, help_text='Track if first login email was sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"

    def format_phone(self):
        """Format Australian phone number for display."""
        if not self.phone:
            return ''
        phone = self.phone.replace(' ', '').replace('-', '')
        if phone.startswith('04') or phone.startswith('02') or phone.startswith('07'):
            return f"{phone[:2]} {phone[2:6]} {phone[6:]}"
        return phone


class Customer(models.Model):
    """Legacy customer model for non-authenticated bookings."""
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
