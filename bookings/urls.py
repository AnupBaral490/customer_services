from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('booking/', views.BookingCreateView.as_view(), name='booking-create'),
    path('booking/success/', views.booking_success, name='booking-success'),
    path('booking/<int:booking_id>/cancel/', views.booking_cancel_view, name='booking-cancel'),
    path('booking/<int:booking_id>/reminder/', views.booking_reminder_view, name='booking-reminder'),
    path('quote/', views.quote_request_view, name='quote-request'),
    path('quote/success/', views.quote_success, name='quote-success'),
]
