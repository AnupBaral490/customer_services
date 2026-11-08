from django.db import models
from django.utils import timezone
from customers.models import Customer
from services.models import Service
import uuid


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PROPERTY_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('office', 'Office'),
        ('commercial', 'Commercial'),
        ('other', 'Other'),
    ]

    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    property_size = models.CharField(max_length=100, blank=True, help_text="e.g., '100 sqm'")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    additional_requirements = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    internal_notes = models.TextField(blank=True)
    assigned_staff = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Bookings'

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"BK{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.customer.full_name}"


class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    FREQUENCY_CHOICES = [
        ('once', 'One-time'),
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quote_requests')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    property_type = models.CharField(max_length=20, choices=Booking.PROPERTY_CHOICES)
    cleaning_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    suburb = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    additional_requirements = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    estimated_quote = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f"Quote - {self.customer.full_name}"
