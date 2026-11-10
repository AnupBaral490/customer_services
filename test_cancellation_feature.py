#!/usr/bin/env python
"""
Test script for booking cancellation feature.
Tests the refund policy calculation and model methods.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.config.settings')
sys.path.insert(0, 'c:\\cleaning_services\\config')
django.setup()

from django.utils import timezone
from bookings.models import Booking, QuoteRequest
from customers.models import Customer
from services.models import Service


def test_refund_policy():
    """Test refund policy calculation."""
    print("\n" + "="*60)
    print("TESTING BOOKING CANCELLATION FEATURE")
    print("="*60)
    
    # Create test customer and service
    customer, _ = Customer.objects.get_or_create(
        email='test.cancellation@example.com',
        defaults={
            'full_name': 'Test Cancellation Customer',
            'phone': '0412345678',
            'address': '123 Test St',
            'suburb': 'Test Suburb',
            'postcode': '1234'
        }
    )
    
    service = Service.objects.first()
    if not service:
        print("❌ No services found. Please create a service first.")
        return
    
    print(f"\n✓ Using customer: {customer.full_name}")
    print(f"✓ Using service: {service.name}")
    
    # Test 1: Booking more than 7 days away
    print("\n" + "-"*60)
    print("TEST 1: Booking More Than 7 Days Away")
    print("-"*60)
    
    future_date = (timezone.now() + timedelta(days=10)).date()
    booking1 = Booking.objects.create(
        customer=customer,
        service=service,
        property_type='house',
        preferred_date=future_date,
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    
    days = booking1.get_days_until_booking()
    refund_type, refund_percent, refund_desc = booking1.get_refund_policy()
    
    print(f"Booking reference: {booking1.booking_reference}")
    print(f"Appointment date: {booking1.preferred_date}")
    print(f"Days until booking: {days}")
    print(f"Refund type: {refund_type}")
    print(f"Refund percentage: {refund_percent}%")
    print(f"Policy description: {refund_desc}")
    
    assert days > 7, f"Expected >7 days, got {days}"
    assert refund_type == 'full_refund', f"Expected full_refund, got {refund_type}"
    assert refund_percent == 100, f"Expected 100%, got {refund_percent}%"
    print("✅ PASSED: Full refund policy correct")
    
    # Test 2: Booking 3-7 days away
    print("\n" + "-"*60)
    print("TEST 2: Booking 3-7 Days Away")
    print("-"*60)
    
    mid_date = (timezone.now() + timedelta(days=5)).date()
    booking2 = Booking.objects.create(
        customer=customer,
        service=service,
        property_type='apartment',
        preferred_date=mid_date,
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    
    days = booking2.get_days_until_booking()
    refund_type, refund_percent, refund_desc = booking2.get_refund_policy()
    
    print(f"Booking reference: {booking2.booking_reference}")
    print(f"Appointment date: {booking2.preferred_date}")
    print(f"Days until booking: {days}")
    print(f"Refund type: {refund_type}")
    print(f"Refund percentage: {refund_percent}%")
    print(f"Policy description: {refund_desc}")
    
    assert 3 <= days <= 7, f"Expected 3-7 days, got {days}"
    assert refund_type == 'fifty_percent', f"Expected fifty_percent, got {refund_type}"
    assert refund_percent == 50, f"Expected 50%, got {refund_percent}%"
    print("✅ PASSED: 50% refund policy correct")
    
    # Test 3: Booking less than 3 days away
    print("\n" + "-"*60)
    print("TEST 3: Booking Less Than 3 Days Away")
    print("-"*60)
    
    soon_date = (timezone.now() + timedelta(days=1)).date()
    booking3 = Booking.objects.create(
        customer=customer,
        service=service,
        property_type='office',
        preferred_date=soon_date,
        preferred_time=timezone.now().time(),
        status='confirmed'
    )
    
    days = booking3.get_days_until_booking()
    refund_type, refund_percent, refund_desc = booking3.get_refund_policy()
    
    print(f"Booking reference: {booking3.booking_reference}")
    print(f"Appointment date: {booking3.preferred_date}")
    print(f"Days until booking: {days}")
    print(f"Refund type: {refund_type}")
    print(f"Refund percentage: {refund_percent}%")
    print(f"Policy description: {refund_desc}")
    
    assert days < 3, f"Expected <3 days, got {days}"
    assert refund_type == 'no_refund', f"Expected no_refund, got {refund_type}"
    assert refund_percent == 0, f"Expected 0%, got {refund_percent}%"
    print("✅ PASSED: No refund policy correct")
    
    # Test 4: Cancellation workflow
    print("\n" + "-"*60)
    print("TEST 4: Cancellation Workflow")
    print("-"*60)
    
    print(f"Before cancellation:")
    print(f"  is_cancelled: {booking1.is_cancelled}")
    print(f"  status: {booking1.status}")
    print(f"  refund_status: {booking1.refund_status}")
    
    # Simulate cancellation
    booking1.is_cancelled = True
    booking1.cancelled_at = timezone.now()
    booking1.status = 'cancelled'
    booking1.cancellation_reason = 'schedule_conflict'
    booking1.cancellation_requested_by = 'customer'
    refund_type, _, _ = booking1.get_refund_policy()
    booking1.refund_status = refund_type
    booking1.refund_amount = '100%'
    booking1.save()
    
    # Reload from DB
    booking1.refresh_from_db()
    
    print(f"\nAfter cancellation:")
    print(f"  is_cancelled: {booking1.is_cancelled}")
    print(f"  cancelled_at: {booking1.cancelled_at}")
    print(f"  status: {booking1.status}")
    print(f"  refund_status: {booking1.refund_status}")
    print(f"  cancellation_reason: {booking1.cancellation_reason}")
    print(f"  cancellation_requested_by: {booking1.cancellation_requested_by}")
    print(f"  refund_amount: {booking1.refund_amount}")
    
    assert booking1.is_cancelled == True, "Expected is_cancelled=True"
    assert booking1.status == 'cancelled', f"Expected status='cancelled', got {booking1.status}"
    assert booking1.refund_status == 'full_refund', f"Expected full_refund, got {booking1.refund_status}"
    print("✅ PASSED: Cancellation workflow correct")
    
    # Test 5: Can be cancelled checks
    print("\n" + "-"*60)
    print("TEST 5: Cancellation Eligibility Checks")
    print("-"*60)
    
    # Create bookings with different statuses
    test_statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
    
    for status in test_statuses:
        test_booking = Booking.objects.create(
            customer=customer,
            service=service,
            property_type='house',
            preferred_date=(timezone.now() + timedelta(days=5)).date(),
            preferred_time=timezone.now().time(),
            status=status
        )
        
        can_cancel = test_booking.can_be_cancelled()
        print(f"Status: {status:15} → Can cancel: {can_cancel}")
        
        if status in ['completed', 'cancelled']:
            assert not can_cancel, f"Expected can_cancel=False for {status}"
        else:
            assert can_cancel, f"Expected can_cancel=True for {status}"
    
    print("✅ PASSED: Cancellation eligibility checks correct")
    
    # Summary
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✅")
    print("="*60)
    print("\nFeature Summary:")
    print("✓ Refund policy correctly calculated based on booking date")
    print("✓ Full refund for >7 days")
    print("✓ 50% refund for 3-7 days")
    print("✓ No refund for <3 days")
    print("✓ Cancellation workflow updates all fields correctly")
    print("✓ Cancellation eligibility checks work correctly")
    print("\n✅ Booking cancellation feature is working correctly!")


if __name__ == '__main__':
    try:
        test_refund_policy()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
