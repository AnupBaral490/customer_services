from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking, QuoteRequest
from .forms import BookingForm, BookingCustomerForm, QuoteRequestForm, QuoteRequestCustomerForm
from customers.models import Customer
from services.models import Service


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

            # Send confirmation email
            self._send_booking_email(booking, customer)

            messages.success(self.request, 'Your booking request has been submitted successfully!')
            self.object = booking
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def _send_booking_email(self, booking, customer):
        try:
            subject = f'Booking Confirmation - {booking.booking_reference}'
            message = f"""
Hello {customer.full_name},

Thank you for requesting a booking with {settings.BUSINESS_NAME}.

Booking Reference: {booking.booking_reference}
Service: {booking.service.name}
Preferred Date: {booking.preferred_date.strftime('%d/%m/%Y')}
Preferred Time: {booking.preferred_time.strftime('%H:%M')}
Status: Pending Confirmation

We will confirm your booking soon. If you have any questions, please contact us at {settings.BUSINESS_PHONE}.

Best regards,
{settings.BUSINESS_NAME}
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer.email])
        except Exception as e:
            print(f"Error sending email: {e}")


def booking_success(request):
    return render(request, 'bookings/booking-success.html')


def quote_request_view(request):
    if request.method == 'POST':
        customer_form = QuoteRequestCustomerForm(request.POST)
        quote_form = QuoteRequestForm(request.POST)

        if customer_form.is_valid() and quote_form.is_valid():
            customer = customer_form.save()
            quote = quote_form.save(commit=False)
            quote.customer = customer
            quote.save()

            # Send confirmation email
            try:
                subject = f'Quote Request Received - {settings.BUSINESS_NAME}'
                message = f"""
Hello {customer.full_name},

Thank you for requesting a quote from {settings.BUSINESS_NAME}.

We have received your quote request and will review your requirements shortly. 
We will contact you within 24-48 hours with a personalized quote.

Service: {quote.service.name}
Property Type: {quote.get_property_type_display()}
Suburb: {quote.suburb}

If you have any urgent questions, please contact us at {settings.BUSINESS_PHONE}.

Best regards,
{settings.BUSINESS_NAME}
"""
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer.email])
            except Exception as e:
                print(f"Error sending email: {e}")

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


def quote_success(request):
    return render(request, 'bookings/quote-success.html')
