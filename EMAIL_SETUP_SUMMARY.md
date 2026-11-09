# Email System Setup - Complete Guide

## What Was Changed

### 1. Email Backend Configuration
- **Default**: Console backend (prints emails to terminal for testing)
- **Environment Variable**: Can be switched to SMTP backend for production
- **File**: `config/config/settings.py` (lines 130-145)

### 2. Email Sending Functions
Enhanced with better error handling and logging:
- `send_welcome_email()` - Sent on signup
- `send_first_login_email()` - Sent on first login (only once per customer)
- Both functions now log errors properly

### 3. Phone Validation
- Accepts any phone number with 7+ digits
- Perfect for testing without valid Australian numbers
- Updated in: `customers/forms.py`, `bookings/forms.py`, `contact/forms.py`

## Current Email System Status

✅ **Working Features:**
- Welcome email sent on signup (appears in console)
- First login email sent only once per customer
- Booking confirmation emails
- Quote request acknowledgment emails
- Admin notification emails
- All emails have professional HTML templates with company branding

## How to Test Emails (Right Now)

The system is currently configured to **print emails to the console**. This is perfect for testing.

### Step 1: Sign Up a New Account
1. Navigate to: http://localhost:8000/customers/signup/
2. Use test phone number: `1234567` (or any 7+ digits)
3. Fill in email, name, password
4. Click "Sign Up"

### Step 2: Check Console Output
The welcome email will appear in your terminal where Django is running:

```
Content-Type: text/html; charset="utf-8"
Subject: Welcome to Premium Cleaning Services
From: baralanup832@gmail.com
To: your-test-email@example.com

<html>
    <body>... full email content ...</body>
</html>
```

### Step 3: Test First Login Email
1. Logout from your account
2. Login again with the same credentials
3. Check console for first login email (appears only once)

## Switching to Gmail for Production

### Phase 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow Google's setup wizard
4. Verify with your phone number

### Phase 2: Create App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select app: "Mail"
3. Select device: "Windows Computer" (or your device)
4. Google generates a 16-character password (example: `lszg npgx cdfx vbmu`)
5. **Copy this password** (won't be shown again)

### Phase 3: Update Environment Configuration
Create a `.env` file in the project root:

```env
# Email Configuration - Switch to SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=baralanup832@gmail.com
EMAIL_HOST_PASSWORD=lszg npgx cdfx vbmu
DEFAULT_FROM_EMAIL=baralanup832@gmail.com
```

### Phase 4: Restart Django Server
```bash
# Stop the running server (Ctrl+C)
# Then restart it
python manage.py runserver
```

### Phase 5: Test Email Sending
Sign up a new account and check your actual email inbox (not console).

## Email Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER ACTIONS                         │
└─────────────────────────────────────────────────────────┘
              ↓                    ↓                   ↓
         [SIGNUP]            [LOGIN]            [BOOKING]
              ↓                    ↓                   ↓
    [send_welcome_email]  [send_first_login_email]  [send_booking_email]
              ↓                    ↓                   ↓
         ┌────────────────────────────────────────────────┐
         │    EMAIL BACKEND (Console or SMTP)             │
         ├────────────────────────────────────────────────┤
         │ Console: Print to terminal (for testing)       │
         │ SMTP:    Send via Gmail (for production)       │
         └────────────────────────────────────────────────┘
              ↓                    ↓                   ↓
         [CONSOLE]            [GMAIL]            [CUSTOMER]
```

## Email Content Templates

All emails use professional HTML templates with:
- Company branding and color scheme (#183D39, #DCA85C)
- Clear call-to-action buttons
- Contact information footer
- Mobile-responsive design

### Email Types:
1. **Welcome Email** - Sent immediately after signup
2. **First Login Email** - Sent once on first login
3. **Booking Confirmation** - Sent when booking is confirmed
4. **Quote Request Confirmation** - Sent when quote is requested
5. **Admin Notifications** - Sent to admin for bookings/quotes

## File Changes Summary

| File | Change | Purpose |
|------|--------|---------|
| `config/config/settings.py` | Console backend default + env vars | Flexible email configuration |
| `customers/views.py` | Added logging + error handling | Better debugging |
| `.env.example` | Updated with instructions | Clear setup guide |
| `EMAIL_TROUBLESHOOTING.md` | New file | Comprehensive troubleshooting guide |

## Troubleshooting

### I don't see emails in console
- Check that Django server is running in your terminal
- Scroll up in terminal to find the email output
- Emails print to the same terminal where `python manage.py runserver` runs

### Emails worked but now I switched to SMTP and nothing happens
1. Check `.env` file exists and has correct values
2. Verify Gmail app password is exactly right (spaces matter: `lszg npgx cdfx vbmu`)
3. Ensure 2-Factor Authentication is enabled on Gmail
4. Restart Django server after changing `.env`

### Getting an error about SMTP
- Check EMAIL_PORT=587 (not 465)
- Check EMAIL_USE_TLS=True
- Verify EMAIL_HOST=smtp.gmail.com

### Still not receiving emails to real Gmail?
1. Check spam folder
2. Allow less secure apps: https://myaccount.google.com/security
3. Try sending a test email from Gmail to verify account is working
4. Contact Google support if 2-Factor setup has issues

## Next Steps

1. **Test with Console Backend** (current setup)
   - Sign up a test account
   - Verify emails appear in console
   
2. **When Ready for Production**
   - Follow "Switching to Gmail for Production" section
   - Create `.env` file with Gmail credentials
   - Test real email delivery

3. **Production Best Practices**
   - Use professional email service (SendGrid, Mailgun)
   - Set up domain records (SPF, DKIM, DMARC)
   - Monitor email delivery rates
   - Implement email verification

## Quick Reference

**To test emails:**
```bash
# Terminal 1: Run Django
cd config
python manage.py runserver

# Terminal 2: Check emails in Terminal 1's output
# Sign up at http://localhost:8000/customers/signup/
```

**To switch to Gmail:**
1. Create `.env` with `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
2. Add Gmail app password to `.env`
3. Restart Django
4. Test signup - email should arrive in Gmail inbox

**To verify setup:**
```python
# In Django shell
from django.core.mail import send_mail
result = send_mail('Test', 'Test email', 'baralanup832@gmail.com', ['test@example.com'])
print(result)  # Should print 1
```

## Customer Features

Customers can now:
- ✅ Sign up with flexible phone validation (7+ digits)
- ✅ Receive welcome email automatically
- ✅ Get notified on first login
- ✅ Book appointments and receive confirmations
- ✅ Request quotes and get acknowledgments
- ✅ See all emails with professional branding
- ✅ Access profile management features

