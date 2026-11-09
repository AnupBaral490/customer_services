# Email Troubleshooting Guide

## Current Status
- **Email Backend**: Console (default for testing)
- **From Address**: baralanup832@gmail.com
- **Backend Type**: Configurable via environment variable

## Email System Features
✅ Welcome email sent on signup  
✅ First login notification (sent once per customer)  
✅ Booking confirmation emails  
✅ Quote request acknowledgment emails  
✅ Admin notification emails  

## Testing the Email System

### Option 1: Console Backend (Recommended for Testing)
The default configuration outputs emails to the console. When you:
- Sign up a new account
- First login to an account

You'll see the email content printed in your terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome to Premium Cleaning Services
From: baralanup832@gmail.com
To: test@example.com
Date: ...

[EMAIL BODY HERE]
```

### Option 2: Gmail SMTP (Production)

To switch to Gmail SMTP:

1. **Enable 2-Factor Authentication** on your Gmail account
   - Visit: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Create an App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Google generates a 16-character password
   - Copy this password (it won't be shown again)

3. **Create a `.env` file** in the project root:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=baralanup832@gmail.com
   EMAIL_HOST_PASSWORD=lszg npgx cdfx vbmu
   DEFAULT_FROM_EMAIL=baralanup832@gmail.com
   ```

4. **Restart the Django server** after updating `.env`

## Troubleshooting Checklist

### Emails showing in console but not being sent to Gmail?
1. Check that EMAIL_BACKEND is set to `django.core.mail.backends.smtp.EmailBackend`
2. Verify the Gmail account has 2-Factor Authentication enabled
3. Ensure you're using an App Password (not your Gmail password)
4. Check Gmail spam folder
5. Try sending a test email:
   ```bash
   python manage.py shell
   from django.core.mail import send_mail
   result = send_mail('Test', 'This is a test email', 'baralanup832@gmail.com', ['youremail@example.com'])
   print(f'Sent: {result}')
   ```

### Getting "SMTPAuthenticationError"?
- App password is incorrect or contains typos
- 2-Factor Authentication not enabled on Gmail
- Using Gmail password instead of App Password

### Getting "SMTPException: SMTP AUTH extension not supported"?
- EMAIL_USE_TLS is not set to True
- Email port might be wrong (should be 587, not 465)

### Email address keeps showing the sender as Gmail?
- Make sure DEFAULT_FROM_EMAIL matches EMAIL_HOST_USER
- Some email providers have restrictions on sender addresses

## Phone Number Validation

Phone validation is flexible for testing. Accepts any number with 7+ digits:
- ✅ 1234567
- ✅ 0412345678
- ✅ +61412345678
- ❌ 123456 (too short)

This allows testing without valid Australian phone numbers.

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Emails in console but not sent | Console backend is active | Change EMAIL_BACKEND to SMTP |
| "Invalid app password" error | Wrong credentials | Regenerate app password at Google account |
| Emails taking forever | Gmail rate limiting | Wait between test emails |
| Emails in spam folder | Gmail filtering | Add sender to contacts or whitelist |
| No first login email | Profile not created properly | Ensure migration 0003 is applied |

## Email Flow

1. **Signup** → Welcome email sent immediately
2. **First Login** → First login notification email sent (only once)
3. **Booking** → Confirmation to customer + Admin notification
4. **Quote Request** → Confirmation to customer + Admin notification
5. **Contact Form** → Confirmation to visitor + Admin notification

## Configuration Files

- `config/config/settings.py` - Email configuration (lines 130+)
- `.env` - Environment-specific settings (create if needed)
- `.env.example` - Template for `.env` file

## For Production Deployment

Before deploying to production:
1. Use a dedicated business email service (SendGrid, Mailgun, AWS SES)
2. Configure SPF, DKIM, DMARC records for domain
3. Monitor bounce rates and spam complaints
4. Use email verification links in accounts
5. Implement unsubscribe functionality

