#!/usr/bin/env python
"""
Create a test booking to test the confirmation feature.
"""
import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from bookings.models import Booking
from customers.models import Customer
from services.models import Service

print("\n" + "="*80)
print("CREATE TEST BOOKING")
print("="*80)

try:
    # Get first customer
    customer = Customer.objects.first()
    if not customer:
        print("✗ No customers found.")
        sys.exit(1)
    
    # Get first service
    service = Service.objects.first()
    if not service:
        print("✗ No services found.")
        sys.exit(1)
    
    # Create a new booking for testing
    booking = Booking.objects.create(
        customer=customer,
        service=service,
        property_type='house',
        bedrooms=3,
        bathrooms=2,
        property_size='150 sqm',
        preferred_date=datetime.now().date() + timedelta(days=7),
        preferred_time=datetime.now().time().replace(hour=10, minute=0),
        additional_requirements='Test booking for confirmation email feature',
        status='pending'
    )
    
    print(f"\n✓ Test booking created!")
    print(f"  Booking Reference: {booking.booking_reference}")
    print(f"  Customer: {customer.full_name} ({customer.email})")
    print(f"  Service: {service.name}")
    print(f"  Status: {booking.status}")
    print(f"  Date: {booking.preferred_date}")
    print(f"  Time: {booking.preferred_time.strftime('%H:%M')}")
    
    print("\n" + "="*80)
    print("NEXT STEP: Run test_booking_confirmation.py to confirm it")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
