from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from bookings.models import Booking, QuoteRequest
from contact.models import ContactMessage
from customers.models import Customer
from services.models import Service
from django.utils import timezone
from datetime import timedelta


@login_required(login_url='admin:login')
def dashboard(request):
    """Main dashboard view with statistics."""
    now = timezone.now()
    this_month_start = now.replace(day=1)

    # Statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    total_quote_requests = QuoteRequest.objects.count()
    total_customers = Customer.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    # Recent data
    recent_bookings = Booking.objects.select_related('customer', 'service')[:5]
    recent_quotes = QuoteRequest.objects.select_related('customer', 'service')[:5]
    upcoming_bookings = Booking.objects.filter(
        preferred_date__gte=now.date(),
        status__in=['confirmed', 'in_progress']
    ).select_related('customer', 'service').order_by('preferred_date')[:5]

    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'total_quote_requests': total_quote_requests,
        'total_customers': total_customers,
        'unread_messages': unread_messages,
        'recent_bookings': recent_bookings,
        'recent_quotes': recent_quotes,
        'upcoming_bookings': upcoming_bookings,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='admin:login')
def bookings_list(request):
    """List all bookings with filtering and search."""
    bookings = Booking.objects.select_related('customer', 'service').all()

    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    property_filter = request.GET.get('property_type')
    if property_filter:
        bookings = bookings.filter(property_type=property_filter)

    # Search
    search = request.GET.get('search')
    if search:
        bookings = bookings.filter(
            Q(booking_reference__icontains=search) |
            Q(customer__full_name__icontains=search) |
            Q(customer__email__icontains=search)
        )

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page
    total_pages = (bookings.count() + per_page - 1) // per_page

    context = {
        'bookings': bookings[start:end],
        'total_bookings': bookings.count(),
        'current_page': int(page),
        'total_pages': total_pages,
        'status_choices': Booking.STATUS_CHOICES,
        'property_choices': Booking.PROPERTY_CHOICES,
    }

    return render(request, 'dashboard/bookings-list.html', context)


@login_required(login_url='admin:login')
def quotes_list(request):
    """List all quote requests."""
    quotes = QuoteRequest.objects.select_related('customer', 'service').all()

    status_filter = request.GET.get('status')
    if status_filter:
        quotes = quotes.filter(status=status_filter)

    search = request.GET.get('search')
    if search:
        quotes = quotes.filter(
            Q(customer__full_name__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(suburb__icontains=search)
        )

    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page
    total_pages = (quotes.count() + per_page - 1) // per_page

    context = {
        'quotes': quotes[start:end],
        'total_quotes': quotes.count(),
        'current_page': int(page),
        'total_pages': total_pages,
        'status_choices': QuoteRequest.STATUS_CHOICES,
    }

    return render(request, 'dashboard/quotes-list.html', context)


@login_required(login_url='admin:login')
def messages_list(request):
    """List all contact messages."""
    messages = ContactMessage.objects.all()

    search = request.GET.get('search')
    if search:
        messages = messages.filter(
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search)
        )

    unread_only = request.GET.get('unread') == 'on'
    if unread_only:
        messages = messages.filter(is_read=False)

    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page
    total_pages = (messages.count() + per_page - 1) // per_page

    context = {
        'messages': messages[start:end],
        'total_messages': messages.count(),
        'unread_count': ContactMessage.objects.filter(is_read=False).count(),
        'current_page': int(page),
        'total_pages': total_pages,
    }

    return render(request, 'dashboard/messages-list.html', context)
