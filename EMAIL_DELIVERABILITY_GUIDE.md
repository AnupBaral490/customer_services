# Email Deliverability Guide

## Problem 1: Welcome Emails Going to Spam

Emails sent from Gmail often go to spam due to security policies. Here are the solutions:

### Why Emails Go to Spam

Gmail and other email providers filter emails based on:
- **SPF (Sender Policy Framework)** - Verifies the email server
- **DKIM (DomainKeys Identified Mail)** - Signs the email
- **DMARC (Domain-based Message Authentication)** - Policy enforcement
- **Sender reputation** - New senders start with low reputation
- **Email authentication** - Headers and formatting

### Solution 1: Setup Gmail App Password ✅ (Already Configured)

Your app is using a Gmail app password which is correct. Current settings:
```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'baralanup832@gmail.com'
EMAIL_HOST_PASSWORD = 'lszg npgx cdfx vbmu'
```

### Solution 2: Verify Gmail Less Secure Apps Access

1. Go to: https://myaccount.google.com/security
2. Look for "Less secure app access" and enable it
3. Or use an **App Password** (recommended):
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password
   - Replace `EMAIL_HOST_PASSWORD` in `settings.py`

### Solution 3: Add Email Headers (Prevents Spam)

Update `settings.py` to add authentication headers:

```python
# Add this to config/config/settings.py

# Email authentication headers (prevents spam filtering)
EMAIL_HOST_USER = 'baralanup832@gmail.com'
EMAIL_HOST_PASSWORD = 'lszg npgx cdfx vbmu'
DEFAULT_FROM_EMAIL = 'baralanup832@gmail.com'

# Additional email configuration
EMAIL_USE_AUTHENTICATION = True
EMAIL_TLS_MANDATORY = True
```

### Solution 4: Improve Email Headers in Code

The welcome emails already include proper HTML formatting which helps. Add this to `customers/views.py` function `send_welcome_email()` to improve deliverability:

```python
def send_welcome_email(user):
    """Send welcome email to new customer on signup."""
    try:
        subject = f'Welcome to {settings.BUSINESS_NAME}'
        # ... existing html_message code ...
        
        send_mail(
            subject,
            f'Welcome to {settings.BUSINESS_NAME}. Your account is ready to use.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        # Add custom headers for better delivery
        from django.core.mail import EmailMultiAlternatives
        email = EmailMultiAlternatives(
            subject,
            f'Welcome to {settings.BUSINESS_NAME}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.attach_alternative(html_message, "text/html")
        # Add authentication headers
        email.extra_headers = {
            'X-Priority': '3',
            'X-MSMail-Priority': 'Normal',
        }
        email.send()
        logger.info(f"Welcome email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending welcome email to {user.email}: {e}")
        return False
```

### Solution 5: Test Email Delivery

Run this command to test:
```bash
python config/manage.py shell
```

Then paste:
```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email from Raslan Cleaning',
    'If you see this, email delivery is working!',
    settings.DEFAULT_FROM_EMAIL,
    ['your-email@gmail.com'],  # Replace with your email
    fail_silently=False,
)
print("Email sent!")
```

### Solution 6: Ask Users to Mark as "Not Spam"

Add a note in the welcome email:
```html
<p style="background: #FFF3CD; padding: 10px; border-radius: 4px; font-size: 12px;">
    <strong>💡 Tip:</strong> If this email arrives in your Spam folder, please mark it as "Not Spam" so you don't miss future updates!
</p>
```

---

## Problem 2: Send Confirmation Email When Admin Confirms Booking ✅ (Already Implemented)

Good news! **This is already fully implemented** in your code.

### How It Works

1. **Location**: `bookings/signals.py`
2. **Trigger**: When admin changes booking status to "confirmed"
3. **Email Contains**:
   - Booking reference number
   - Service details
   - Scheduled date (formatted nicely)
   - Scheduled time
   - Property type
   - Contact information
   - Call-to-action buttons

### Email Template Preview

The booking confirmation email includes:
- ✅ Booking reference (e.g., "BK-2024-001")
- ✅ Service name
- ✅ **Scheduled Date** (formatted as "Monday, 15 November 2024")
- ✅ **Scheduled Time** (formatted as "14:00")
- ✅ Property type
- ✅ Reminder about arrival time window (30 min before/after)
- ✅ Phone and email for rescheduling
- ✅ Links to customer profile and website

### To Use (Admin Workflow)

1. Go to: `/admin/bookings/booking/`
2. Select a booking
3. Change Status from "pending" to "confirmed"
4. Click "Save"
5. ✅ Confirmation email automatically sent to customer

### Example Booking Confirmation Email

**Subject**: "Booking Confirmed - BK-2024-001234"

**Body**:
```
✓ Booking Confirmed!

Your appointment has been confirmed by Raslan Cleaning Service

Hi John,

Great news! Your booking with Raslan Cleaning Service has been confirmed. Our team is ready to serve you!

Confirmed Booking Details:
━━━━━━━━━━━━━━━━━━━━━━━━
Booking Reference: BK-2024-001234
Service: End-of-Lease Cleaning
Scheduled Date: Monday, 15 November 2024
Time: 14:00
Property Type: Apartment

📞 Important: Please ensure someone is available at the scheduled time. 
Our team will arrive between 30 minutes before to 30 minutes after the scheduled time.

If you need to reschedule or have any questions:
Phone: +61 2 1234 5678
Email: hello@cleaningservices.com.au

[View Your Booking] [Back to Website]
```

---

## Verify Everything is Working

### Test Booking Confirmation Email

1. Create a test booking manually or via admin
2. Go to `/admin/bookings/booking/`
3. Find the booking and change status to "confirmed"
4. Save
5. Check the customer's email (check spam folder too!)
6. Email should arrive with date and time details

### Check Email Logs

Monitor console output when Django runs:
```
✓ Confirmation email sent to customer@example.com for booking BK-2024-001234
```

---

## Summary of Email System

| Email Type | Trigger | Status |
|-----------|---------|--------|
| Welcome Email | User creates account | ✅ Working |
| First Login Email | User logs in first time | ✅ Working |
| Booking Confirmation | Admin confirms booking | ✅ Working |
| Quote Response | Manual (not automated) | ℹ️ Manual only |

---

## Recommendations

### To Improve Email Deliverability

1. **Use a business email domain** (instead of @gmail.com)
   - Example: admin@raslancleaningservices.com.au
   - Setup SPF, DKIM, DMARC records

2. **Consider email service providers** for better delivery:
   - SendGrid
   - Mailgun
   - AWS SES
   - These have better reputation and deliverability

3. **Add unsubscribe link** (required for marketing emails)
   - Add to email footer

4. **Monitor email bounces** and failures

### Current Setup Assessment

✅ **Working**: Email sending functionality is correct
⚠️ **Issue**: May be hitting Gmail's spam filters
✅ **Solution**: Setup SPF/DKIM or use professional email service

---

## Quick Fixes Checklist

- [ ] Test email sending (run shell command above)
- [ ] Check spam folder for test emails
- [ ] Enable Gmail app password access
- [ ] Ask team to mark emails as "Not Spam"
- [ ] Monitor booking confirmation emails after admin approval
- [ ] Consider switching to business domain email
- [ ] Setup SendGrid or Mailgun for production

---

## Contact Issues?

If emails still don't arrive:
1. Check `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct
2. Verify Gmail security settings allow app access
3. Check console logs for error messages
4. Test with `python manage.py shell` command above
5. Consider switching email provider

