#!/usr/bin/env python
"""
Test script to verify email system is working.
Run from config folder: python ../test_email_system.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

print("=" * 60)
print("EMAIL SYSTEM TEST")
print("=" * 60)

# Check email configuration
print(f"\n📧 Email Backend: {settings.EMAIL_BACKEND}")
print(f"📧 Email Host: {settings.EMAIL_HOST}")
print(f"📧 Email Port: {settings.EMAIL_PORT}")
print(f"📧 Default From Email: {settings.DEFAULT_FROM_EMAIL}")

# Determine if using console or SMTP
backend_name = settings.EMAIL_BACKEND.split('.')[-1]
if backend_name == 'ConsoleEmailBackend':
    print(f"✅ Console backend active - emails will print to console")
elif backend_name == 'EmailBackend':  # SMTP
    print(f"✅ SMTP backend active - emails will be sent to Gmail")
else:
    print(f"⚠️  Unknown backend: {backend_name}")

print("\n" + "=" * 60)
print("SENDING TEST EMAIL...")
print("=" * 60)

try:
    result = send_mail(
        'Test Email from Cleaning Services',
        'This is a test email to verify the email system is working correctly.',
        settings.DEFAULT_FROM_EMAIL,
        ['test@example.com'],
        fail_silently=False,
    )
    
    if result:
        print(f"✅ Test email sent successfully!")
        if 'Console' in backend_name:
            print("💡 Check console output above for full email content")
        else:
            print("💡 Check test@example.com inbox for the email")
    else:
        print(f"❌ Failed to send test email")
except Exception as e:
    print(f"❌ Error sending test email: {e}")

print("\n" + "=" * 60)
print("CHECKING EXISTING USERS...")
print("=" * 60)

users = User.objects.all()
print(f"Total users in database: {users.count()}")

for user in users[:5]:  # Show first 5 users
    print(f"  • {user.username} ({user.email})")

if users.count() > 5:
    print(f"  ... and {users.count() - 5} more")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nTo switch email backends:")
print("1. Console (testing):  Set EMAIL_BACKEND in settings.py or .env")
print("2. Gmail (production): Set EMAIL_BACKEND and update credentials in .env")
print("\nSee EMAIL_TROUBLESHOOTING.md for detailed configuration guide")
