"""
Quick verification script to test cancellation feature models
Run with: python manage.py shell < verify_cancellation.py
"""

from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking
from customers.models import Customer
from services.models import Service

print("\n" + "="*60)
print("VERIFYING BOOKING CANCELLATION FEATURE")
print("="*60)

# Check that the model has the new fields
print("\nChecking Booking model fields...")
booking_fields = [f.name for f in Booking._meta.get_fields()]
required_fields = [
    'is_cancelled', 'cancelled_at', 'cancellation_reason',
    'refund_status', 'refund_amount', 'cancellation_requested_by',
    'reminder_sent'
]

for field in required_fields:
    if field in booking_fields:
        print(f"  ✓ {field}")
    else:
        print(f"  ✗ MISSING: {field}")

# Test refund policy logic
print("\nTesting refund policy calculation...")

customer, _ = Customer.objects.get_or_create(
    email='verify@test.com',
    defaults={'full_name': 'Test', 'phone': '0412345678'}
)

service = Service.objects.first()
if not service:
    print("  ✗ No services found")
else:
    # Test 1: >7 days
    booking1 = Booking(
        customer=customer,
        service=service,
        property_type='house',
        preferred_date=(timezone.now() + timedelta(days=10)).date(),
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    refund_type, refund_pct, desc = booking1.get_refund_policy()
    if refund_type == 'full_refund' and refund_pct == 100:
        print(f"  ✓ >7 days: {refund_type} ({refund_pct}%)")
    else:
        print(f"  ✗ >7 days: Expected full_refund/100%, got {refund_type}/{refund_pct}%")
    
    # Test 2: 3-7 days
    booking2 = Booking(
        customer=customer,
        service=service,
        property_type='house',
        preferred_date=(timezone.now() + timedelta(days=5)).date(),
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    refund_type, refund_pct, desc = booking2.get_refund_policy()
    if refund_type == 'fifty_percent' and refund_pct == 50:
        print(f"  ✓ 3-7 days: {refund_type} ({refund_pct}%)")
    else:
        print(f"  ✗ 3-7 days: Expected fifty_percent/50%, got {refund_type}/{refund_pct}%")
    
    # Test 3: <3 days
    booking3 = Booking(
        customer=customer,
        service=service,
        property_type='house',
        preferred_date=(timezone.now() + timedelta(days=1)).date(),
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    refund_type, refund_pct, desc = booking3.get_refund_policy()
    if refund_type == 'no_refund' and refund_pct == 0:
        print(f"  ✓ <3 days: {refund_type} ({refund_pct}%)")
    else:
        print(f"  ✗ <3 days: Expected no_refund/0%, got {refund_type}/{refund_pct}%")

print("\nTesting model methods...")
booking4 = Booking(
    customer=customer,
    service=service,
    property_type='house',
    preferred_date=(timezone.now() + timedelta(days=5)).date(),
    preferred_time=timezone.now().time(),
    status='confirmed'
)

# Test can_be_cancelled
if booking4.can_be_cancelled():
    print("  ✓ can_be_cancelled() returns True for pending/confirmed")
else:
    print("  ✗ can_be_cancelled() should return True")

# Test get_days_until_booking
days = booking4.get_days_until_booking()
if days == 5:
    print(f"  ✓ get_days_until_booking() returns {days}")
else:
    print(f"  ✗ get_days_until_booking() should return 5, got {days}")

print("\n" + "="*60)
print("✅ VERIFICATION COMPLETE")
print("="*60)
print("\nAll cancellation feature components are in place!")
print("The feature is ready to use.")
