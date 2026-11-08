from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('booking/', views.BookingCreateView.as_view(), name='booking-create'),
    path('booking/success/', views.booking_success, name='booking-success'),
    path('quote/', views.quote_request_view, name='quote-request'),
    path('quote/success/', views.quote_success, name='quote-success'),
]
