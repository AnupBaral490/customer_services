from django.contrib import admin
from .models import Booking, QuoteRequest


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'customer', 'service', 'status', 'preferred_date', 'created_at')
    list_filter = ('status', 'preferred_date', 'property_type', 'created_at')
    search_fields = ('booking_reference', 'customer__full_name', 'customer__email')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Details', {
            'fields': ('booking_reference', 'customer', 'service', 'status')
        }),
        ('Property Information', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'property_size')
        }),
        ('Scheduling', {
            'fields': ('preferred_date', 'preferred_time')
        }),
        ('Additional Information', {
            'fields': ('additional_requirements', 'assigned_staff', 'internal_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'status', 'cleaning_frequency', 'suburb', 'created_at')
    list_filter = ('status', 'cleaning_frequency', 'created_at')
    search_fields = ('customer__full_name', 'customer__email', 'suburb')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Customer Details', {
            'fields': ('customer', 'service')
        }),
        ('Property Information', {
            'fields': ('property_type', 'suburb', 'postcode')
        }),
        ('Service Details', {
            'fields': ('cleaning_frequency', 'additional_requirements')
        }),
        ('Quote Status', {
            'fields': ('status', 'estimated_quote')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
