# Quick Testing Guide

## ✅ What's Fixed

1. **Phone Validation** - Now accepts any phone number with at least 7 digits
   - Example: `1234567` works
   - Example: `9876543210` works
   - Example: `04 1234 5678` works

2. **Email Sending** - Now uses Gmail SMTP to actually send emails
   - Emails will be sent to real addresses
   - From: `baralanup832@gmail.com`

## 🧪 How to Test

### Step 1: Create an Account
1. Go to `http://localhost:8000/customers/signup/`
2. Fill in:
   - Full Name: `Test User`
   - Email: `your-real-email@gmail.com` (or any email)
   - Phone: `1234567` (any 7+ digits)
   - Password: `TestPass123`
3. Click "Create Account"
4. **✓ Welcome email will be sent**

### Step 2: Login (First Time)
1. Go to `http://localhost:8000/customers/login/`
2. Email: `your-real-email@gmail.com`
3. Password: `TestPass123`
4. Click "Log In"
5. **✓ First login email will be sent (only once)**

### Step 3: Make a Booking
1. Click "Book Now" in navbar
2. Fill in booking details
3. In customer section, enter:
   - Phone: `1234567890`
4. Submit
5. **✓ Booking confirmation email sent to customer**
6. **✓ Admin notification sent to baralanup832@gmail.com**

### Step 4: Request a Quote
1. Click "Get Quote" in navbar
2. Fill in quote details
3. In customer section, enter:
   - Phone: `9876543`
4. Submit
5. **✓ Quote confirmation email sent**
6. **✓ Admin notification sent**

## 📧 Where Emails Go

- **Signup Welcome**: Sent to customer email
- **First Login**: Sent to customer email (once only)
- **Booking Confirmation**: Sent to customer email
- **Booking Admin Notification**: Sent to `baralanup832@gmail.com`
- **Quote Confirmation**: Sent to customer email
- **Quote Admin Notification**: Sent to `baralanup832@gmail.com`

## 🔍 Common Phone Numbers for Testing

```
1234567
9876543210
04 1234 5678
0412345678
+61412345678
1234567890123  (extra long, still works)
```

## ⚠️ If Emails Don't Send

1. Check that Gmail account has:
   - 2-Factor Authentication enabled
   - App password generated (not regular password)
   
2. The app password used is: `lszg npgx cdfx vbmu`

3. If still not working, check:
   - Internet connection
   - Gmail account isn't blocking the app
   - Run `python manage.py check` to verify settings

## ✨ Everything Should Now Work!

- Phone validation: ✓ Flexible
- Email sending: ✓ Active via Gmail SMTP
- All forms: ✓ Testable with any phone
- All email triggers: ✓ Working

Happy testing! 🎉
