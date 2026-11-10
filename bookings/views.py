from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Booking, QuoteRequest
from .forms import BookingForm, BookingCustomerForm, QuoteRequestForm, QuoteRequestCustomerForm, BookingCancellationForm
from customers.models import Customer
from services.models import Service


@method_decorator(login_required, name='dispatch')
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking-form.html'
    success_url = reverse_lazy('bookings:booking-success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            if 'customer_form' not in context:
                context['customer_form'] = BookingCustomerForm(self.request.POST)
        else:
            context['customer_form'] = BookingCustomerForm()
        context['services'] = Service.objects.filter(is_active=True)
        context['service_id'] = self.request.GET.get('service_id')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer_form = context['customer_form']

        if customer_form.is_valid():
            customer = customer_form.save()
            booking = form.save(commit=False)
            booking.customer = customer
            booking.save()

            # Send confirmation emails
            self._send_booking_email(booking, customer)
            self._send_admin_notification(booking, customer)

            messages.success(self.request, 'Your booking request has been submitted successfully!')
            self.object = booking
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def _send_booking_email(self, booking, customer):
        """Send professional HTML booking confirmation to customer."""
        try:
            subject = f'Booking Confirmation - {booking.booking_reference}'
            html_message = f"""
            <html>
                <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Booking Confirmed!</h1>
                            <p style="color: #666; margin: 0; font-size: 16px;">Your appointment has been received</p>
                        </div>

                        <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #10B981;">
                            <p style="margin-bottom: 15px;">Hi {customer.full_name},</p>
                            
                            <p style="margin-bottom: 20px;">Thank you for booking with <strong>{settings.BUSINESS_NAME}</strong>. We have received your booking request and will confirm it within 24 hours.</p>

                            <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                                <h3 style="margin-top: 0; color: #183D39;">Booking Details:</h3>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Reference:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right; color: #183D39; font-weight: 700;">{booking.booking_reference}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Service:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{booking.service.name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Date:</strong></td>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{booking.preferred_date.strftime('%A, %d %B %Y')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;"><strong>Time:</strong></td>
                                        <td style="padding: 8px 0; text-align: right;">{booking.preferred_time.strftime('%H:%M')}</td>
                                    </tr>
                                </table>
                            </div>

                            <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; border-radius: 4px; margin: 20px 0;">
                                <p style="margin: 0;"><strong>Status:</strong> Pending Confirmation</p>
                                <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">We will contact you to confirm your appointment.</p>
                            </div>

                            <p style="margin: 20px 0 0 0;">If you need to make any changes or have questions, please contact us:</p>
                            <p style="margin: 0;">
                                <strong>Phone:</strong> {settings.BUSINESS_PHONE}<br>
                                <strong>Email:</strong> {settings.BUSINESS_EMAIL}
                            </p>
                        </div>

                        <div style="text-align: center; margin-top: 30px;">
                            <a href="{settings.SITE_URL}/customers/profile/" 
                               style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                                View Your Bookings
                            </a>
                        </div>

                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                            <p style="margin: 0;">
                                <strong>{settings.BUSINESS_NAME}</strong><br>
                                {settings.BUSINESS_ADDRESS}<br>
                                Phone: {settings.BUSINESS_PHONE}
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            send_mail(
                subject,
                f'Your booking {booking.booking_reference} has been received.',
                settings.DEFAULT_FROM_EMAIL,
                [customer.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending booking email: {e}")

    def _send_admin_notification(self, booking, customer):
        """Send admin notification about new booking."""
        try:
            subject = f'New Booking - {booking.booking_reference}'
            html_message = f"""
            <html>
                <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">New Booking Received</h1>
                        </div>

                        <div style="background: white; padding: 30px; border-radius: 8px;">
                            <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                                <h3 style="margin-top: 0; color: #183D39;">Customer Information:</h3>
                                <p style="margin: 5px 0;"><strong>Name:</strong> {customer.full_name}</p>
                                <p style="margin: 5px 0;"><strong>Email:</strong> {customer.email}</p>
                                <p style="margin: 5px 0;"><strong>Phone:</strong> {customer.phone}</p>
                                <p style="margin: 5px 0;"><strong>Address:</strong> {customer.address}, {customer.suburb} {customer.postcode}</p>
                            </div>

                            <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                                <h3 style="margin-top: 0; color: #183D39;">Booking Details:</h3>
                                <p style="margin: 5px 0;"><strong>Reference:</strong> {booking.booking_reference}</p>
                                <p style="margin: 5px 0;"><strong>Service:</strong> {booking.service.name}</p>
                                <p style="margin: 5px 0;"><strong>Date:</strong> {booking.preferred_date.strftime('%d/%m/%Y')}</p>
                                <p style="margin: 5px 0;"><strong>Time:</strong> {booking.preferred_time.strftime('%H:%M')}</p>
                                <p style="margin: 5px 0;"><strong>Status:</strong> Pending</p>
                            </div>
                        </div>

                        <div style="text-align: center; margin-top: 20px;">
                            <a href="{settings.SITE_URL}/admin/bookings/booking/{booking.id}/change/" 
                               style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                                View in Admin
                            </a>
                        </div>
                    </div>
                </body>
            </html>
            """
            send_mail(
                subject,
                f'New booking {booking.booking_reference} from {customer.full_name}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.BUSINESS_EMAIL],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending admin notification: {e}")


def booking_success(request):
    return render(request, 'bookings/booking-success.html')


@login_required
def quote_request_view(request):
    if request.method == 'POST':
        customer_form = QuoteRequestCustomerForm(request.POST)
        quote_form = QuoteRequestForm(request.POST)

        if customer_form.is_valid() and quote_form.is_valid():
            customer = customer_form.save()
            quote = quote_form.save(commit=False)
            quote.customer = customer
            quote.save()

            # Send confirmation emails
            send_quote_confirmation_email(customer, quote)
            send_quote_admin_notification(customer, quote)

            messages.success(request, 'Your quote request has been submitted successfully!')
            return redirect('bookings:quote-success')
    else:
        customer_form = QuoteRequestCustomerForm()
        quote_form = QuoteRequestForm()

    context = {
        'customer_form': customer_form,
        'quote_form': quote_form,
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'bookings/quote-request-form.html', context)


def send_quote_confirmation_email(customer, quote):
    """Send professional HTML quote confirmation to customer."""
    try:
        subject = f'Quote Request Received - {settings.BUSINESS_NAME}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Quote Request Received!</h1>
                        <p style="color: #666; margin: 0; font-size: 16px;">We'll get back to you shortly</p>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #3B82F6;">
                        <p style="margin-bottom: 15px;">Hi {customer.full_name},</p>
                        
                        <p style="margin-bottom: 20px;">Thank you for requesting a quote from <strong>{settings.BUSINESS_NAME}</strong>. We have received your request and our team will review it shortly.</p>

                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Your Request Details:</h3>
                            <p style="margin: 5px 0;"><strong>Service:</strong> {quote.service.name}</p>
                            <p style="margin: 5px 0;"><strong>Property Type:</strong> {quote.get_property_type_display()}</p>
                            <p style="margin: 5px 0;"><strong>Location:</strong> {quote.suburb}</p>
                            <p style="margin: 5px 0;"><strong>Frequency:</strong> {quote.get_frequency_display() if hasattr(quote, 'frequency') else 'One-time'}</p>
                        </div>

                        <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; border-radius: 4px; margin: 20px 0;">
                            <p style="margin: 0;"><strong>Next Steps:</strong> Our team will contact you within 24-48 hours with a personalized quote.</p>
                        </div>

                        <p style="margin: 20px 0 0 0;">If you have any questions in the meantime, please don't hesitate to contact us:</p>
                        <p style="margin: 0;">
                            <strong>Phone:</strong> {settings.BUSINESS_PHONE}<br>
                            <strong>Email:</strong> {settings.BUSINESS_EMAIL}
                        </p>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="{settings.SITE_URL}/customers/profile/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            View Your Quotes
                        </a>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                        <p style="margin: 0;">
                            <strong>{settings.BUSINESS_NAME}</strong><br>
                            {settings.BUSINESS_ADDRESS}<br>
                            Phone: {settings.BUSINESS_PHONE}
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        send_mail(
            subject,
            f'Your quote request has been received by {settings.BUSINESS_NAME}.',
            settings.DEFAULT_FROM_EMAIL,
            [customer.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending quote email: {e}")


def send_quote_admin_notification(customer, quote):
    """Send admin notification about new quote request."""
    try:
        subject = f'New Quote Request - {quote.service.name}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">New Quote Request</h1>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px;">
                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Customer Information:</h3>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {customer.full_name}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {customer.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {customer.phone}</p>
                        </div>

                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Quote Details:</h3>
                            <p style="margin: 5px 0;"><strong>Service:</strong> {quote.service.name}</p>
                            <p style="margin: 5px 0;"><strong>Property Type:</strong> {quote.get_property_type_display()}</p>
                            <p style="margin: 5px 0;"><strong>Location:</strong> {quote.suburb}</p>
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 20px;">
                        <a href="{settings.SITE_URL}/admin/bookings/quoterequest/{quote.id}/change/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            View in Admin
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
        send_mail(
            subject,
            f'New quote request from {customer.full_name}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.BUSINESS_EMAIL],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending admin quote notification: {e}")


def quote_success(request):
    return render(request, 'bookings/quote-success.html')


@login_required
def booking_cancel_view(request, booking_id):
    """Allow customers to cancel their bookings."""
    booking = get_object_or_404(Booking, id=booking_id, customer__email=request.user.email)
    
    if not booking.can_be_cancelled():
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('customers:customer-profile')
    
    if request.method == 'POST':
        form = BookingCancellationForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            additional_details = form.cleaned_data['additional_details']
            
            # Mark booking as cancelled
            booking.is_cancelled = True
            booking.cancelled_at = timezone.now()
            booking.cancellation_reason = reason
            booking.status = 'cancelled'
            booking.cancellation_requested_by = 'customer'
            
            # Calculate refund policy
            refund_type, refund_percent, refund_desc = booking.get_refund_policy()
            booking.refund_status = refund_type
            booking.refund_amount = f"{refund_percent}%"
            
            if additional_details:
                booking.internal_notes = f"Customer notes: {additional_details}\n\nOriginal notes: {booking.internal_notes}"
            
            booking.save()
            
            # Send confirmation emails
            _send_cancellation_confirmation_email(booking, refund_type, refund_desc)
            _send_cancellation_admin_notification(booking, reason, additional_details, refund_type)
            
            messages.success(request, 'Your booking has been cancelled successfully. You will receive a confirmation email shortly.')
            return redirect('customers:customer-profile')
    else:
        form = BookingCancellationForm()
    
    # Get refund policy info
    refund_type, refund_percent, refund_desc = booking.get_refund_policy()
    days_until = booking.get_days_until_booking()
    
    context = {
        'booking': booking,
        'form': form,
        'refund_type': refund_type,
        'refund_percent': refund_percent,
        'refund_desc': refund_desc,
        'days_until': days_until,
    }
    
    return render(request, 'bookings/booking-cancellation.html', context)


def _send_cancellation_confirmation_email(booking, refund_type, refund_desc):
    """Send cancellation confirmation to customer."""
    try:
        refund_message = ""
        if refund_type == 'full_refund':
            refund_message = "You are eligible for a <strong>full refund</strong> or to reschedule without any penalty."
        elif refund_type == 'fifty_percent':
            refund_message = "You are eligible for a <strong>50% refund</strong>. Rescheduling is subject to availability."
        else:
            refund_message = "Unfortunately, <strong>no refund</strong> is applicable as per the cancellation policy. Your booking fee will be retained."
        
        subject = f'Booking Cancellation Confirmed - {booking.booking_reference}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Booking Cancelled</h1>
                        <p style="color: #666; margin: 0; font-size: 16px;">Your cancellation request has been processed</p>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #EF4444;">
                        <p style="margin-bottom: 15px;">Hi {booking.customer.full_name},</p>
                        
                        <p style="margin-bottom: 20px;">Your booking {booking.booking_reference} has been successfully cancelled as of {timezone.now().strftime('%d %B %Y at %H:%M')}.</p>

                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Booking Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Reference:</strong></td>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{booking.booking_reference}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Original Date:</strong></td>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{booking.preferred_date.strftime('%d %B %Y')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8;"><strong>Service:</strong></td>
                                    <td style="padding: 8px 0; border-bottom: 1px solid #E8E8E8; text-align: right;">{booking.service.name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px 0;"><strong>Cancellation Date:</strong></td>
                                    <td style="padding: 8px 0; text-align: right;">{timezone.now().strftime('%d %B %Y')}</td>
                                </tr>
                            </table>
                        </div>

                        <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; border-radius: 4px; margin: 20px 0;">
                            <h4 style="margin-top: 0; color: #92400E;">Refund Policy:</h4>
                            <p style="margin: 0;">{refund_message}</p>
                        </div>

                        <p style="margin: 20px 0 0 0;">If you would like to reschedule your appointment or have any questions, please contact us:</p>
                        <p style="margin: 0;">
                            <strong>Phone:</strong> {settings.BUSINESS_PHONE}<br>
                            <strong>Email:</strong> {settings.BUSINESS_EMAIL}
                        </p>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="{settings.SITE_URL}/bookings/booking/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            Book Again
                        </a>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                        <p style="margin: 0;">
                            <strong>{settings.BUSINESS_NAME}</strong><br>
                            {settings.BUSINESS_ADDRESS}<br>
                            Phone: {settings.BUSINESS_PHONE}
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        send_mail(
            subject,
            f'Your booking {booking.booking_reference} has been cancelled.',
            settings.DEFAULT_FROM_EMAIL,
            [booking.customer.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending cancellation confirmation email: {e}")


def _send_cancellation_admin_notification(booking, reason, additional_details, refund_type):
    """Send admin notification about booking cancellation."""
    try:
        subject = f'Booking Cancelled - {booking.booking_reference}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Booking Cancelled</h1>
                        <p style="color: #666; margin: 0; font-size: 16px;">Customer-initiated cancellation</p>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px;">
                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Customer Information:</h3>
                            <p style="margin: 5px 0;"><strong>Name:</strong> {booking.customer.full_name}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {booking.customer.email}</p>
                            <p style="margin: 5px 0;"><strong>Phone:</strong> {booking.customer.phone}</p>
                        </div>

                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">Booking Details:</h3>
                            <p style="margin: 5px 0;"><strong>Reference:</strong> {booking.booking_reference}</p>
                            <p style="margin: 5px 0;"><strong>Original Date:</strong> {booking.preferred_date.strftime('%d/%m/%Y')}</p>
                            <p style="margin: 5px 0;"><strong>Service:</strong> {booking.service.name}</p>
                            <p style="margin: 5px 0;"><strong>Cancellation Reason:</strong> {reason.replace('_', ' ').title()}</p>
                            <p style="margin: 5px 0;"><strong>Refund Type:</strong> {refund_type.replace('_', ' ').title()}</p>
                            {f'<p style="margin: 5px 0;"><strong>Additional Notes:</strong> {additional_details}</p>' if additional_details else ''}
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 20px;">
                        <a href="{settings.SITE_URL}/admin/bookings/booking/{booking.id}/change/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 10px 25px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            View in Admin
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
        send_mail(
            subject,
            f'Booking {booking.booking_reference} has been cancelled by {booking.customer.full_name}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.BUSINESS_EMAIL],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending cancellation admin notification: {e}")


@login_required
def booking_reminder_view(request, booking_id):
    """Display booking with cancellation policy reminder to customer."""
    booking = get_object_or_404(Booking, id=booking_id, customer__email=request.user.email)
    
    # Get refund policy info
    refund_type, refund_percent, refund_desc = booking.get_refund_policy()
    days_until = booking.get_days_until_booking()
    can_cancel = booking.can_be_cancelled()
    
    # Mark reminder as sent
    if not booking.reminder_sent and booking.status in ['confirmed', 'pending']:
        booking.reminder_sent = True
        booking.save(update_fields=['reminder_sent'])
    
    context = {
        'booking': booking,
        'refund_type': refund_type,
        'refund_percent': refund_percent,
        'refund_desc': refund_desc,
        'days_until': days_until,
        'can_cancel': can_cancel,
    }
    
    return render(request, 'bookings/booking-reminder.html', context)
