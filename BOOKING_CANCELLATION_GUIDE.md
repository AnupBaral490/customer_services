# Booking Cancellation & Refund Policy Feature

## Overview
This guide explains the booking cancellation feature that allows customers to cancel their appointments with a tiered refund policy based on how far in advance they cancel.

## Features Implemented

### 1. **Tiered Refund Policy**
The system automatically calculates refund eligibility based on days until booking:

- **More than 7 days before**: 100% refund or reschedule without penalty
- **3-7 days before**: 50% refund or reschedule subject to availability
- **Less than 3 days before**: No refund (booking fee retained)

### 2. **Customer-Facing Cancellation Interface**
- Customers can view their bookings on their profile
- Each booking has "Reminder" and "Cancel" buttons
- Dedicated cancellation page with policy details
- Form to capture cancellation reason and feedback
- Clear confirmation of refund eligibility before cancellation

### 3. **Reminder Notices**
- View cancellation policy reminder page
- Shows current refund eligibility
- Complete policy table for reference
- Links to contact support if they want to reschedule instead

### 4. **Email Notifications**
- Customer receives cancellation confirmation with refund details
- Admin receives notification of cancellations
- All refund information included in emails

### 5. **Admin Management**
- Track cancelled bookings in Django admin
- View refund status and amounts
- See cancellation reason and customer feedback
- Track who initiated the cancellation (customer or admin)

## Database Model Updates

### New Booking Fields

```python
is_cancelled = BooleanField(default=False)
cancelled_at = DateTimeField(null=True, blank=True)
cancellation_reason = TextField(blank=True)
refund_status = CharField(choices=[...], default='not_applicable')
refund_amount = CharField(blank=True)
cancellation_requested_by = CharField(choices=[('customer', 'Customer'), ('admin', 'Admin')])
reminder_sent = BooleanField(default=False)
```

### New Model Methods

```python
get_days_until_booking()  # Days remaining until appointment
get_refund_policy()       # Returns (refund_type, percentage, description)
can_be_cancelled()        # Checks if booking is eligible for cancellation
get_cancellation_allowed_until()  # Returns deadline for cancellation (24 hours before)
```

## URL Routes

```
/bookings/booking/<id>/cancel/     - Cancellation form
/bookings/booking/<id>/reminder/   - Policy reminder page
```

## Templates

### booking-cancellation.html
- Main cancellation page
- Shows booking summary
- Displays applicable refund policy
- Captures cancellation reason
- Requires confirmation checkbox

### booking-reminder.html
- Policy reminder page
- Shows current refund eligibility
- Complete refund policy table
- Contact information for support

### Updated customer/profile.html
- Added "Actions" column to bookings table
- Added reminder and cancel buttons
- Shows cancelled status when applicable

## Using the Feature

### For Customers

#### View Cancellation Policy
1. Go to "My Profile"
2. Click bell icon (📋) next to any booking to view the cancellation policy reminder

#### Cancel a Booking
1. Go to "My Profile"
2. Click the X icon (❌) next to the booking you want to cancel
3. Select your cancellation reason
4. (Optional) Add additional details
5. Check the confirmation checkbox
6. Click "Confirm Cancellation"
7. Receive confirmation email with refund details

### For Admin

#### View Cancelled Bookings
1. Navigate to Django Admin → Bookings
2. Filter by "Cancelled" status
3. View refund_status to see refund eligibility
4. Click on booking to see full cancellation details

#### Manual Cancellation (if needed)
1. Open booking in Django admin
2. Set is_cancelled = True
3. Set status = 'cancelled'
4. Select refund_status
5. Set cancellation_requested_by = 'admin'
6. Save the booking

## Email Examples

### Cancellation Confirmation Email
- Booking reference and details
- Cancellation date
- Refund eligibility based on policy
- Instructions for rescheduling
- Contact information

### Admin Notification Email
- Customer information
- Booking details
- Cancellation reason
- Refund type
- Link to admin interface

## Forms

### BookingCancellationForm
Fields:
- **reason**: Required radio selection from:
  - Schedule Conflict
  - No Longer Needed
  - Found Alternative Service
  - Financial Reasons
  - Other Reason
- **additional_details**: Optional textarea for feedback
- **confirm_cancellation**: Required checkbox confirmation

## Key Business Logic

### Refund Calculation
```python
days_until = booking.get_days_until_booking()

if days_until > 7:
    refund_type = 'full_refund'
    refund_percent = 100
elif days_until >= 3:
    refund_type = 'fifty_percent'
    refund_percent = 50
else:
    refund_type = 'no_refund'
    refund_percent = 0
```

### Cancellation Validation
- Only pending, confirmed, or in_progress bookings can be cancelled
- Completed and already cancelled bookings cannot be cancelled again
- Must be logged in as the customer who made the booking

### Timeline
- **Booking created**: No cancellation info yet
- **Customer cancels**: Updates is_cancelled, cancelled_at, refund_status
- **Email sent**: Customer and admin notified
- **Reminder checked**: Marks reminder_sent = True

## Testing

### Test Scenario 1: Full Refund (>7 days)
1. Create a booking for 10 days from now
2. Click cancel button
3. Verify refund policy shows "100% Refund"
4. Complete cancellation
5. Check email shows full refund eligibility

### Test Scenario 2: 50% Refund (3-7 days)
1. Create a booking for 5 days from now
2. Click cancel button
3. Verify refund policy shows "50% Refund"
4. Complete cancellation
5. Check email shows 50% refund eligibility

### Test Scenario 3: No Refund (<3 days)
1. Create a booking for 2 days from now
2. Click cancel button
3. Verify refund policy shows "No Refund"
4. Complete cancellation
5. Check email shows no refund eligibility

### Test Scenario 4: View Reminder (No Cancel)
1. Create a booking
2. Click reminder button
3. Verify all policy information displays correctly
4. Verify you can still cancel from this page

## Customer Communication

### Cancellation Policy Statement (suggest for cancellation policy page)
```
Cancellation Policy

We understand that plans can change. That's why we offer a flexible 
cancellation policy:

• More than 7 days before: Full refund or reschedule without penalty
• 3-7 days before: 50% refund or reschedule subject to availability
• Less than 3 days before: No refund (booking fee retained)

All cancellations must be made at least 24 hours before your scheduled 
appointment. Refunds are typically processed within 5-7 business days.

For questions or to reschedule, please contact us at [PHONE] or [EMAIL]
```

## Admin Commands

### Check Cancelled Bookings
```bash
python manage.py shell
>>> from bookings.models import Booking
>>> cancelled = Booking.objects.filter(is_cancelled=True)
>>> cancelled.count()  # Total cancelled
```

### Find Bookings by Refund Status
```bash
>>> full_refunds = Booking.objects.filter(refund_status='full_refund')
>>> fifty_percent = Booking.objects.filter(refund_status='fifty_percent')
>>> no_refunds = Booking.objects.filter(refund_status='no_refund')
```

## Integration Points

### Required Settings (already in place)
- DEFAULT_FROM_EMAIL
- BUSINESS_EMAIL
- BUSINESS_NAME
- BUSINESS_PHONE
- SITE_URL

### Email Configuration
The feature uses Django's email sending which should be configured in settings.py for Gmail or your email provider.

## Future Enhancements

Potential improvements:
1. **Automated reminders**: Send email 7 days, 3 days, and 1 day before
2. **Refund processing workflow**: Admin approval/rejection of refunds
3. **Automatic rescheduling**: Let customers pick new dates before cancelling
4. **Partial refund options**: Offer store credit instead of refund
5. **Cancellation statistics**: Dashboard showing cancellation trends
6. **SMS notifications**: Send cancellation confirmations via SMS
7. **Refund method tracking**: Track payment method for refunds
8. **Dispute resolution**: Workflow for cancellation disputes

## Troubleshooting

### Issue: "This booking cannot be cancelled"
**Solution**: Check if the booking is in a completed or already cancelled status. Only pending/confirmed/in_progress bookings can be cancelled.

### Issue: Refund policy showing incorrect amount
**Solution**: Verify the booking.preferred_date is set correctly. The system calculates days from today to preferred_date.

### Issue: Email not sending
**Solution**: Check email configuration in settings.py. Test with:
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test', 'from@example.com', ['to@example.com'])
```

### Issue: Customer can cancel after 24-hour window
**Solution**: The is_cancelled and cancelled_at fields track if cancelled, but the 24-hour deadline is informational. To enforce it, add validation in the view:
```python
from django.utils import timezone
from datetime import timedelta

booking_time = make_aware(datetime.combine(booking.preferred_date, booking.preferred_time))
if timezone.now() > booking_time - timedelta(hours=24):
    # Prevent cancellation
```

## Support

For issues or questions about this feature:
1. Check the Troubleshooting section above
2. Review the code in bookings/views.py
3. Check booking model methods
4. Review email templates in bookings/views.py
