from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .models import Booking, QuoteRequest
from .forms import BookingForm, BookingCustomerForm, QuoteRequestForm, QuoteRequestCustomerForm
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
