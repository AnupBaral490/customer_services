# URGENT: Email Not Arriving - Quick Fix

## Status
✅ Emails ARE being sent by Django  
✅ Gmail SMTP is working perfectly  
❌ Gmail is BLOCKING delivery to inbox  

---

## Quick Fix (Do This NOW)

### Option A: Enable "Less Secure Apps" (1 minute)
1. Go to: **https://myaccount.google.com/security**
2. Scroll down and find "**Less secure app access**"
3. Click it and turn it **ON**
4. Wait 10 minutes
5. Go to: http://localhost:8000/bookings/booking/
6. Make a test booking
7. **Check your Gmail inbox** - email should arrive!

---

### Option B: Use Separate Gmail Account (5 minutes)
If Option A doesn't work:

1. Create new Gmail at: https://accounts.google.com
   - Use name like: `cleaning-noreply` or `cleaning-system`
   
2. Enable 2-Factor Auth on new account:
   - Go to: https://myaccount.google.com/security
   - Set up 2-Step Verification
   
3. Create App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select: Mail + Windows Computer
   - Copy the 16-char password
   
4. Update `config/config/settings.py`:
   ```python
   EMAIL_HOST_USER = 'your-new-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-16-char-password'
   ```
   
5. Restart Django
   
6. Make a test booking
   
7. **Check Gmail inbox** - email should arrive!

---

## Why This Happens

Gmail doesn't like sending emails from accounts that:
- Send automated emails
- Are sending from outside Gmail's normal usage pattern
- Don't have "Less secure apps" enabled
- Don't have proper authentication setup

---

## Verification It's Working

Our diagnostic confirmed:
```
✓ Connected to SMTP server
✓ TLS connection established
✓ Authentication successful
✓ Email processed: 1
```

The problem is **Gmail's delivery**, not our code.

---

## Do This First

1. Try **Option A** (Less secure apps) - takes 1 minute
2. Wait 10 minutes
3. Make a booking at http://localhost:8000/bookings/booking/
4. Check inbox

If that doesn't work after 15 minutes, use **Option B** (new account).

---

## Full Details

See: `GMAIL_DELIVERY_FIX.md` for complete guide with all options.

