# Email System - Quick Reference

## Your Questions & Answers

### ❓ Q1: Why do signup emails go to spam?

**A**: Gmail filters new senders. This is normal behavior.

**Quick Fix**: 
- Users should mark emails as "Not Spam"
- Check spam folder when testing
- Use app password (already configured ✅)

### ❓ Q2: How to send email when admin confirms booking?

**A**: ✅ **It's already done automatically!**

**How to test**:
```
1. Go to http://localhost:8000/admin/bookings/booking/
2. Click on a booking
3. Change Status: Pending → Confirmed
4. Click Save
5. Email sent! Check customer's email (including spam folder)
```

---

## Email Flow

```
User Creates Account
        ↓
    ✉️ Welcome Email (with HTML)
        ↓
User Logs In
        ↓
    ✉️ First Login Email (once only)
        ↓
Admin Confirms Booking
        ↓
    ✉️ Booking Confirmation Email
        ├─ Booking Reference
        ├─ Service Name
        ├─ 📅 SCHEDULED DATE
        ├─ 🕐 SCHEDULED TIME
        └─ Contact Info
```

---

## Booking Confirmation Email Contains

✅ Booking reference number (BK-2024-001)
✅ Service name
✅ **📅 Scheduled Date** (e.g., "Monday, 15 November 2024")
✅ **🕐 Scheduled Time** (e.g., "14:00")
✅ Property type & details
✅ Reminder about arrival window (±30 min)
✅ Phone & email for rescheduling
✅ Links to profile & website

---

## Email Settings

**Config File**: `config/config/settings.py`

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'baralanup832@gmail.com'
EMAIL_HOST_PASSWORD = 'lszg npgx cdfx vbmu'
DEFAULT_FROM_EMAIL = 'baralanup832@gmail.com'
```

---

## Test Email Sending

```bash
cd config
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'If you see this, emails are working!',
    settings.DEFAULT_FROM_EMAIL,
    ['your-test-email@gmail.com'],
)
print("Email sent!")
```

---

## Admin Workflow to Send Booking Confirmation

### Method 1: Admin Panel
```
URL: http://localhost:8000/admin/bookings/booking/
1. Click booking
2. Status: Pending → Confirmed
3. Save
✓ Email sent automatically
```

### Method 2: Dashboard
```
URL: http://localhost:8000/dashboard/
1. Click "Manage Bookings"
2. Select booking
3. Change status (if interface allows)
✓ Email sent automatically
```

---

## Email Customization

### To Change Email Content:

**Welcome Email**: Edit `customers/views.py` → `send_welcome_email()` function

**Booking Confirmation**: Edit `bookings/signals.py` → `send_booking_confirmation_email()` function

### To Change Sender Email:

`config/config/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### To Add Custom Headers:

`customers/views.py` or `bookings/signals.py`:
```python
from django.core.mail import EmailMultiAlternatives

email = EmailMultiAlternatives(subject, text, from_email, to_list)
email.attach_alternative(html_content, "text/html")
email.extra_headers = {
    'X-Priority': '3',
    'X-Custom-Header': 'value',
}
email.send()
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Emails go to spam | Check spam folder, mark as "Not Spam" |
| Emails don't arrive | Check settings in `settings.py` |
| Wrong sender email | Change `EMAIL_HOST_USER` in `settings.py` |
| Wrong date/time format | Edit templates in views/signals.py |
| Can't send emails | Run test command above, check console |

---

## Files Reference

| File | Purpose |
|------|---------|
| `config/config/settings.py` | Email configuration (SMTP) |
| `customers/views.py` | Welcome & first login emails |
| `bookings/signals.py` | Booking confirmation emails |
| `bookings/apps.py` | Signal registration |
| `bookings/admin.py` | Admin panel setup |

---

## Email Features Status

✅ Signup welcome email - Working
✅ First login email - Working  
✅ Booking confirmation - Working
✅ Includes date & time - Working
✅ Professional HTML design - Working
✅ Customer contact info - Working
✅ Branded with colors - Working

---

## Production Recommendations

1. **Use business domain email** (@raslancleaningservices.com.au)
2. **Setup SPF/DKIM/DMARC** records
3. **Consider SendGrid or Mailgun** for better deliverability
4. **Add unsubscribe link** for marketing compliance
5. **Monitor bounce rates** and failures
6. **Test in multiple email clients** (Gmail, Outlook, etc.)

---

## One-Line Summary

✅ **Emails work! Booking confirmations with date & time send automatically when admin confirms bookings. Signup emails go to spam due to Gmail security (normal behavior).**

