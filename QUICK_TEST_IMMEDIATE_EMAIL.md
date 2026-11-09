# Quick Test - Immediate Email (30 seconds)

## One-Line Test

Admin confirms booking → Email arrives immediately with date & time

---

## Quick Steps

### 1. Open Admin
```
http://localhost:8000/admin/bookings/booking/
```

### 2. Create Test Booking
- Click "Add Booking"
- Customer: Any
- Service: Any
- Status: **Pending**
- Date: Tomorrow
- Time: 10:00
- Click **SAVE**

### 3. Confirm Booking
- Click the booking you just created
- Status: **Pending → Confirmed**
- Click **SAVE**

### 4. Check Results

**In Console (Django Terminal):**
```
✓✓✓ CONFIRMATION EMAIL SENT IMMEDIATELY ✓✓✓
    To: customer@example.com
    Booking: BK-2024-001234
    Date: Monday, 15 November 2024
    Time: 10:00
    Result: 1 email(s) sent
```

**In Email (Check customer inbox/spam):**
```
Subject: Booking Confirmed - BK-2024-001234

Contains:
✓ Booking reference
✓ Service name
✓ Scheduled date: Monday, 15 November 2024
✓ Scheduled time: 10:00
✓ Contact info
```

---

## Success Indicators

✅ Console shows `✓✓✓ CONFIRMATION EMAIL SENT IMMEDIATELY ✓✓✓`
✅ Email arrives in customer inbox or spam folder
✅ Email includes date and time
✅ Takes less than 1 second after clicking Save

---

## If Email Doesn't Arrive

Check:
1. Customer email address in booking (correct?)
2. Spam folder (check there too)
3. Console error message (read it)
4. Gmail settings (app password correct?)

---

## Done!

✅ Email sends immediately when booking confirmed
✅ No delay or queue
✅ Professional format with date & time
✅ Ready to use

