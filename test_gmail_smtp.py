#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("\n" + "="*70)
print("TESTING GMAIL SMTP CONNECTION")
print("="*70)
print(f"\nEmail Backend: {settings.EMAIL_BACKEND}")
print(f"SMTP Host: {settings.EMAIL_HOST}")
print(f"SMTP Port: {settings.EMAIL_PORT}")
print(f"Use TLS: {settings.EMAIL_USE_TLS}")
print(f"From Email: {settings.EMAIL_HOST_USER}")

print("\nAttempting to send test email to anupbaral7777@gmail.com...")

try:
    result = send_mail(
        'Test Connection - Premium Cleaning Services',
        'This is a test email to verify Gmail SMTP is working.',
        settings.DEFAULT_FROM_EMAIL,
        ['anupbaral7777@gmail.com'],
        fail_silently=False,
    )
    print(f"\n✓ SUCCESS! Email sent: {result}")
    print(f"  Check your Gmail inbox for the test email")
    print(f"  (Also check spam/promotions folder)")
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    print(f"\nTroubleshooting:")
    print(f"  1. Is 2-Factor Authentication enabled on Gmail?")
    print(f"  2. Did you create an App Password at myaccount.google.com/apppasswords?")
    print(f"  3. Is the app password exactly: lszg npgx cdfx vbmu?")
    print(f"  4. Check Gmail security settings")

print("\n" + "="*70 + "\n")
