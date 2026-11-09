# Testing Guide - Phone Numbers & Email System

## Phone Number Validation Update

The phone validation has been updated to accept **any phone number with 7+ digits** for flexible testing purposes.

### Accepted Formats

✓ **7+ digits** (minimum): `1234567`
✓ **Local format** (10 digits): `0412345678`
✓ **International format** (11 digits): `+61412345678`
✓ **With spaces/dashes**: `04 1234 5678` or `+61-4-1234-5678`
✓ **Any number combination** as long as total digits ≥ 7

### Test Phone Numbers You Can Use

Here are some test phone numbers you can use for forms (any of these work):

```
Quick Test Numbers:
- 1234567 (simplest, 7 digits)
- 123456789 (9 digits)
- 0412345678 (standard AU format)
- +61412345678 (international format)

Booking Form:
- 0287654321
- +61287654321
- 99999999

Quote Request:
- 0399998888
- 88888888
- 5555555

Contact Form:
- 0755551234
- 1111111
- 7654321
```

### Forms That Use Phone Validation

1. **Customer Signup** (`/customers/signup/`)
   - Phone field: Accepts 7+ digits

2. **Booking Form** (`/bookings/booking/`)
   - Phone field: Accepts 7+ digits

3. **Quote Request** (`/bookings/quote/`)
   - Phone field: Accepts 7+ digits

4. **Contact Form** (`/contact/`)
   - Phone field: Accepts 7+ digits

## Email System Testing

### Current Setup
- **Email Backend:** Console (prints emails to terminal)
- **Mode:** Development/Testing
- **Sender:** baralanup832@gmail.com

### Testing Workflow

#### Step 1: Create a Test Account
1. Go to: **http://localhost:8000/customers/signup/**
2. Fill form:
   - First Name: Test
   - Last Name: User
   - Email: test@example.com (or any email)
   - Phone: **1234567** (or any 7+ digit number)
   - Password: TestPass123
3. Click "Create Account"

#### Step 2: Check for Welcome Email
1. Switch to **Django terminal** (where the server is running)
2. Look for email output with:
   - `Subject: Welcome to Premium Cleaning Services`
   - `To: test@example.com`
   - Full HTML email content below
3. This proves the email system is working!

#### Step 3: Test First Login Email
1. Logout from account
2. Login again with same credentials
3. Check Django terminal for:
   - `Subject: First Login Confirmed - Premium Cleaning Services`
   - Email appears only ONCE per customer

#### Step 4: Test Booking Confirmation Email
1. Click "Book Now" in navbar
2. Fill booking details with test phone: **1234567**
3. Submit form
4. Check Django terminal for booking confirmation email

#### Step 5: Test Quote Request Email
1. Click "Get Quote" in navbar
2. Fill quote details with test phone: **1234567**
3. Submit form
4. Check Django terminal for quote confirmation email

### Where to Find Email Output

**Console emails appear in your Django terminal:**
```
Content-Type: text/html; charset="utf-8"
Subject: Welcome to Premium Cleaning Services
From: baralanup832@gmail.com
To: test@example.com

<html>
    <body>...email HTML content...</body>
</html>
```

### Email Types Sent

| Event | Email | Recipient | When |
|-------|-------|-----------|------|
| Signup | Welcome Email | Customer | Immediately |
| First Login | First Login Notification | Customer | Once per customer |
| Booking | Booking Confirmation | Customer | After booking submitted |
| Booking | Admin Notification | Admin | After booking submitted |
| Quote | Quote Confirmation | Customer | After quote requested |
| Quote | Admin Notification | Admin | After quote requested |

## Switching to Gmail SMTP

To send real emails instead of printing to console:

### 1. Enable 2-Factor Authentication
- Go to: https://myaccount.google.com/security
- Set up 2-Step Verification

### 2. Create App Password
- Go to: https://myaccount.google.com/apppasswords
- Select: Mail + Windows Computer
- Copy the 16-character password

### 3. Create `.env` File
Create file in project root with:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=baralanup832@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### 4. Restart Django Server
- Stop server (Ctrl+C)
- Start again: `python manage.py runserver`

### 5. Test Real Email
- Sign up new account
- Email should arrive in Gmail inbox (check spam folder too)

## Troubleshooting

### Emails Not in Console?
- Check you're looking at Django terminal (not browser console)
- Scroll up to find email output
- Make sure Django server is running

### Can't Find Django Terminal?
Look for window showing:
```
Starting development server at http://localhost:8000/
```

### Getting SMTP Error After Switching to Gmail?
1. Check EMAIL_BACKEND is set to `django.core.mail.backends.smtp.EmailBackend`
2. Verify 2-Factor Authentication is enabled
3. Use App Password (not Gmail password)
4. Ensure `.env` file is in project root
5. Restart Django server

## Complete Testing Checklist

- [ ] Phone validation accepts: 1234567 ✓
- [ ] Can create account with 7-digit phone number
- [ ] Welcome email appears in console
- [ ] Can login to account
- [ ] First login email appears in console (once only)
- [ ] Can make booking with test phone number
- [ ] Booking confirmation email appears
- [ ] Can request quote with test phone number
- [ ] Quote confirmation email appears
- [ ] All emails are HTML formatted
- [ ] All emails contain company branding

## Production Considerations

- [ ] Use professional email service (SendGrid, Mailgun)
- [ ] Configure domain DNS records (SPF, DKIM, DMARC)
- [ ] Implement email verification
- [ ] Add unsubscribe functionality
- [ ] Monitor bounce rates
- [ ] Use real phone validation with SMS verification

## For More Information

- See: **EMAIL_SETUP_SUMMARY.md** - Complete setup guide
- See: **EMAIL_TROUBLESHOOTING.md** - Advanced troubleshooting
- See: **QUICK_EMAIL_TEST.md** - Quick 5-minute test



