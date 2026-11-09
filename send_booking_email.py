#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
django.setup()

from django.core.mail import send_mail
from django.conf import settings

subject = 'Booking Confirmation - Premium Cleaning Services'
html_message = '''
<html>
    <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Booking Confirmed!</h1>
                <p style="color: #666; margin: 0; font-size: 16px;">Your cleaning service appointment is confirmed</p>
            </div>

            <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #10B981;">
                <p style="margin-bottom: 20px;">Hi there,</p>
                
                <p style="margin-bottom: 20px;">Great! Your booking with Premium Cleaning Services has been confirmed. We are excited to help keep your home fresh and clean!</p>

                <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #183D39;">Booking Details:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li><strong>Service:</strong> Professional Cleaning</li>
                        <li><strong>Status:</strong> Confirmed</li>
                        <li><strong>Booking Number:</strong> #BK2026110801</li>
                    </ul>
                </div>

                <p style="margin-bottom: 15px;">What to expect:</p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Our team will arrive on time</li>
                    <li>Professional and thorough cleaning</li>
                    <li>Friendly and courteous service</li>
                    <li>Your satisfaction is guaranteed</li>
                </ul>

                <p style="margin-bottom: 15px;">If you need to reschedule or have any questions, please contact us:</p>
                <p style="margin: 0;">
                    <strong>Phone:</strong> +61 2 1234 5678<br>
                    <strong>Email:</strong> hello@cleaningservices.com.au
                </p>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <a href="http://localhost:8000/customers/profile/" 
                   style="display: inline-block; background: #183D39; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                    View Your Booking
                </a>
            </div>

            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                <p style="margin: 0;">Thank you for choosing Premium Cleaning Services!</p>
                <p style="margin: 5px 0;">This is an automated email. Please do not reply directly.</p>
            </div>
        </div>
    </body>
</html>
'''

print("\n" + "="*70)
print("SENDING BOOKING CONFIRMATION EMAIL")
print("="*70)

try:
    result = send_mail(
        subject,
        'Your booking has been confirmed. View details in the email.',
        settings.DEFAULT_FROM_EMAIL,
        ['anupbaral7777@gmail.com'],
        html_message=html_message,
        fail_silently=False,
    )
    
    print("\n✓ Email sent successfully!")
    print(f"  To: anupbaral7777@gmail.com")
    print(f"  Subject: {subject}")
    print(f"  Backend: {settings.EMAIL_BACKEND}")
    print(f"  Result: {result} email processed")
    print("\n" + "="*70)
    print("NOTE: If using Console backend, check Django terminal for output")
    print("      If using SMTP, check Gmail inbox (also check spam folder)")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n✗ Error: {e}\n")
