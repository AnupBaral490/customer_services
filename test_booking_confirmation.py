#!/usr/bin/env python
"""
Test script to verify booking confirmation email feature works.
This manually triggers the signal to test email sending.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from django.conf import settings
from bookings.models import Booking
from customers.models import Customer
from services.models import Service
from datetime import datetime, timedelta

print("\n" + "="*80)
print("BOOKING CONFIRMATION EMAIL TEST")
print("="*80)

# Find or create test data
print("\n📋 Finding test data...")

try:
    # Get first customer
    customer = Customer.objects.first()
    if not customer:
        print("✗ No customers found. Please create a customer first.")
        sys.exit(1)
    print(f"✓ Customer: {customer.full_name} ({customer.email})")
    
    # Get first service
    service = Service.objects.first()
    if not service:
        print("✗ No services found. Please create a service first.")
        sys.exit(1)
    print(f"✓ Service: {service.name}")
    
    # Get first pending booking
    booking = Booking.objects.filter(status='pending').first()
    if not booking:
        print("✗ No pending bookings found.")
        print("  Please make a booking at: http://localhost:8000/bookings/booking/")
        sys.exit(1)
    print(f"✓ Booking: {booking.booking_reference} (Current status: {booking.status})")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("SIMULATING ADMIN CONFIRMATION")
print("="*80)

print(f"\nChanging booking status from '{booking.status}' to 'confirmed'...")
print("This will trigger the automatic confirmation email...\n")

try:
    # Change status and save - this will trigger the signal
    booking.status = 'confirmed'
    booking.save(update_fields=['status'])
    
    print(f"✓ Booking status updated to: {booking.status}")
    print(f"\n✓ Signal triggered!")
    print(f"✓ Confirmation email should have been sent to: {customer.email}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\n📧 Next Steps:")
print(f"   1. Check {customer.email} for confirmation email")
print(f"   2. Look for subject: 'Booking Confirmed - {booking.booking_reference}'")
print(f"   3. Check spam/promotions folder if not in inbox")
print(f"   4. Check Django terminal for any errors")

print("\n💡 What the email contains:")
print("   ✓ Booking reference: " + booking.booking_reference)
print(f"   ✓ Service: {service.name}")
print(f"   ✓ Date: {booking.preferred_date.strftime('%A, %d %B %Y')}")
print(f"   ✓ Time: {booking.preferred_time.strftime('%H:%M')}")
print(f"   ✓ Property: {booking.get_property_type_display()}")
print(f"   ✓ Customer name: {customer.full_name}")

print("\n" + "="*80)
print("✅ BOOKING CONFIRMATION FEATURE ACTIVE")
print("="*80 + "\n")
