# Quick Email Testing Guide

## 🚀 Test Emails Right Now (5 minutes)

### Step 1: Keep Django Running
```bash
# In terminal 1, Django should already be running
# You'll see: "Starting development server at http://localhost:8000/"
```

### Step 2: Open Browser
Navigate to: **http://localhost:8000/customers/signup/**

### Step 3: Fill Signup Form
- **First Name:** Test
- **Last Name:** User
- **Email:** test@yourdomainhere.com (use any email)
- **Phone:** 1234567 (or any number with 7+ digits)
- **Password:** TestPass123
- **Confirm Password:** TestPass123

### Step 4: Click "Create Account"

### Step 5: Check Terminal
Switch back to Terminal 1 (where Django is running).

**You should see email output:**
```
Content-Type: text/html; charset="utf-8"
Subject: Welcome to Premium Cleaning Services
From: baralanup832@gmail.com
To: test@yourdomainhere.com

<html>
    <body>
        ...welcome email content...
    </body>
</html>
```

## ✅ What This Proves

✅ Email system is working  
✅ Welcome emails are being generated  
✅ Email templates are rendering correctly  
✅ Console backend is active (for testing)  

## 📧 To Send Real Emails to Gmail

### Option A: Quick Test (Without Gmail Setup)
The emails are already printing in console - this proves the system works!

### Option B: Send to Real Gmail (Requires Setup)
1. Go to: https://myaccount.google.com/apppasswords
2. Create an app password (16 characters)
3. Create `.env` file in project root:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=baralanup832@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-password-here
```
4. Restart Django
5. Sign up again - email will go to real Gmail inbox

## 🎯 What Emails Should Arrive

When customer signs up:
- ✅ **Welcome Email** → Immediately

When customer logs in (first time):
- ✅ **First Login Email** → Once per customer

When customer makes booking:
- ✅ **Booking Confirmation** → To customer
- ✅ **Admin Notification** → To admin

## 📱 Test Phone Numbers (All Valid)
- 1234567
- 0412345678
- +61412345678
- 1111111111
- 9876543210

## 🔧 Troubleshooting

### Email not appearing in console?
1. Check Django terminal (not browser console)
2. Scroll up to find the email output
3. Make sure you see "Welcome to Premium Cleaning Services"

### Getting error in console?
1. Django is running fine (you can see the website)
2. Error is normal if Gmail SMTP not configured
3. Switch to console backend - see `.env` instructions above

### Can't find Django terminal?
Look for window with:
```
Starting development server at http://localhost:8000/
```

## 📋 Email Checklist

- [ ] Django server running (can access http://localhost:8000)
- [ ] Can see website homepage
- [ ] Navigate to signup page
- [ ] Fill form with test data
- [ ] Submit form
- [ ] See "Registration successful" message
- [ ] Check Django terminal for email output
- [ ] Email shows welcome message

## 🎉 Success!

If you see the welcome email in console, your email system is working perfectly!

**Next:** Read `EMAIL_SETUP_SUMMARY.md` for advanced configuration.

