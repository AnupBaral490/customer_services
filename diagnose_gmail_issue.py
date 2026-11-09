#!/usr/bin/env python
import os
import sys
import django
import smtplib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("GMAIL SMTP DIAGNOSTIC TOOL")
print("="*80)

print("\n📧 CURRENT EMAIL CONFIGURATION:")
print(f"   Email Backend: {settings.EMAIL_BACKEND}")
print(f"   SMTP Host: {settings.EMAIL_HOST}")
print(f"   SMTP Port: {settings.EMAIL_PORT}")
print(f"   TLS Enabled: {settings.EMAIL_USE_TLS}")
print(f"   From Email: {settings.EMAIL_HOST_USER}")
print(f"   Password: {'*' * len(settings.EMAIL_HOST_PASSWORD)} ({len(settings.EMAIL_HOST_PASSWORD)} chars)")

print("\n🔍 TESTING SMTP CONNECTION...")

try:
    # Test raw SMTP connection
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
    print("   ✓ Connected to SMTP server")
    
    # Test TLS
    server.starttls()
    print("   ✓ TLS connection established")
    
    # Test authentication
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    print("   ✓ Authentication successful")
    
    server.quit()
    print("\n✅ SMTP connection is working correctly!")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ AUTHENTICATION FAILED: {e}")
    print("\n⚠️  SOLUTIONS:")
    print("   1. Go to: https://myaccount.google.com/security")
    print("   2. Enable 2-Factor Authentication")
    print("   3. Go to: https://myaccount.google.com/apppasswords")
    print("   4. Create an App Password for 'Mail' and 'Windows Computer'")
    print("   5. Copy the 16-character password")
    print("   6. Update settings.py EMAIL_HOST_PASSWORD with the new password")
    print(f"   Current password: {settings.EMAIL_HOST_PASSWORD}")
    
except smtplib.SMTPException as e:
    print(f"\n❌ SMTP ERROR: {e}")
    print("\n⚠️  SOLUTIONS:")
    print("   1. Check internet connection")
    print("   2. Verify SMTP host is correct: smtp.gmail.com")
    print("   3. Verify port is correct: 587")
    print("   4. Check firewall/antivirus settings")
    
except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {type(e).__name__}: {e}")

print("\n" + "="*80)
print("TESTING DJANGO EMAIL SENDING...")
print("="*80)

from django.core.mail import send_mail

test_recipients = ['anupbaral7777@gmail.com', 'baralanup832@gmail.com']

for recipient in test_recipients:
    print(f"\nSending test email to: {recipient}")
    try:
        result = send_mail(
            'Test Email - Diagnostic Tool',
            f'If you received this, the email system is working! Recipient: {recipient}',
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        print(f"   ✓ Email processed: {result}")
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {e}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
print("\n💡 NEXT STEPS:")
print("   1. Check your Gmail inbox for test emails")
print("   2. Check Spam/Promotions folders")
print("   3. If still not receiving:")
print("      - Go to: https://myaccount.google.com/security")
print("      - Look for 'Less secure app access' and enable it")
print("      - Or create a new Gmail account specifically for this app")
print("      - Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings")
print("\n" + "="*80 + "\n")
