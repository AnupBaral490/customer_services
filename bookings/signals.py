from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, update_fields, **kwargs):
    """
    Send confirmation email to customer when admin confirms booking.
    Triggered when booking status changes to 'confirmed'.
    """
    
    # Only process updates (not new bookings)
    if created:
        return
    
    # Check if status was changed and is now 'confirmed'
    if update_fields and 'status' in update_fields and instance.status == 'confirmed':
        try:
            customer = instance.customer
            subject = f'Booking Confirmed - {instance.booking_reference}'
            
            html_message = f"""
            <html>
                <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">✓ Booking Confirmed!</h1>
                            <p style="color: #666; margin: 0; font-size: 16px;">Your appointment has been confirmed by {settings.BUSINESS_NAME}</p>
                        </div>

                        <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #10B981;">
                            <p style="margin-bottom: 20px;">Hi {customer.full_name.split()[0] if customer.full_name else 'there'},</p>
                            
                            <p style="margin-bottom: 20px;">Great news! Your booking with <strong>{settings.BUSINESS_NAME}</strong> has been <strong>confirmed</strong>. Our team is ready to serve you!</p>

                            <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                                <h3 style="margin-top: 0; color: #183D39;">Confirmed Booking Details:</h3>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Booking Reference:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right; color: #183D39; font-weight: 700;">{instance.booking_reference}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Service:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{instance.service.name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Scheduled Date:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;"><strong>{instance.preferred_date.strftime('%A, %d %B %Y')}</strong></td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Time:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;"><strong>{instance.preferred_time.strftime('%H:%M')}</strong></td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Property Type:</strong></td>
                                        <td style="padding: 8px 0; text-align: right;">{instance.get_property_type_display()}</td>
                                    </tr>
                                </table>
                            </div>

                            <div style="background: #FFFBEB; border-left: 4px solid #FBBF24; padding: 15px; border-radius: 4px; margin: 20px 0;">
                                <p style="margin: 0;"><strong>📞 Important:</strong></p>
                                <p style="margin: 5px 0 0 0; font-size: 14px;">Please ensure someone is available at the scheduled time. Our team will arrive between 30 minutes before to 30 minutes after the scheduled time.</p>
                            </div>

                            <p style="margin: 20px 0 0 0;">If you need to reschedule or have any questions before your appointment, please contact us immediately:</p>
                            <p style="margin: 0;">
                                <strong>Phone:</strong> <a href="tel:{settings.BUSINESS_PHONE.replace(' ', '')}" style="color: #183D39; text-decoration: none;">{settings.BUSINESS_PHONE}</a><br>
                                <strong>Email:</strong> <a href="mailto:{settings.BUSINESS_EMAIL}" style="color: #183D39; text-decoration: none;">{settings.BUSINESS_EMAIL}</a>
                            </p>
                        </div>

                        <div style="text-align: center; margin-top: 30px;">
                            <a href="{settings.SITE_URL}/customers/profile/" 
                               style="display: inline-block; background: #183D39; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-right: 10px;">
                                View Your Booking
                            </a>
                            <a href="{settings.SITE_URL}/" 
                               style="display: inline-block; background: #DCA85C; color: #183D39; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                                Back to Website
                            </a>
                        </div>

                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                            <p style="margin: 0;">
                                <strong>{settings.BUSINESS_NAME}</strong><br>
                                {settings.BUSINESS_ADDRESS}<br>
                                Phone: {settings.BUSINESS_PHONE}<br>
                                Email: {settings.BUSINESS_EMAIL}
                            </p>
                            <p style="margin: 10px 0 0 0; font-size: 11px; color: #999;">
                                This is an automated confirmation email. Please do not reply directly to this email.
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            send_mail(
                subject,
                f'Your booking {instance.booking_reference} has been confirmed.',
                settings.DEFAULT_FROM_EMAIL,
                [customer.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"✓ Confirmation email sent to {customer.email} for booking {instance.booking_reference}")
            
        except Exception as e:
            print(f"✗ Error sending confirmation email: {e}")
