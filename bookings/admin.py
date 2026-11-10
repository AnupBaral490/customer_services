from django.contrib import admin
from .models import Booking, QuoteRequest


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'customer', 'service', 'status', 'preferred_date', 'refund_status', 'created_at')
    list_filter = ('status', 'refund_status', 'preferred_date', 'property_type', 'created_at', 'is_cancelled')
    search_fields = ('booking_reference', 'customer__full_name', 'customer__email')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at', 'cancelled_at')
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
        ('Cancellation Details', {
            'fields': ('is_cancelled', 'cancelled_at', 'cancellation_reason', 'cancellation_requested_by', 'reminder_sent'),
            'classes': ('collapse',)
        }),
        ('Refund Information', {
            'fields': ('refund_status', 'refund_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make service field read-only after booking is created."""
        readonly = list(self.readonly_fields)
        if obj:  # Editing existing booking
            readonly.append('service')
        return readonly
    
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets based on creation vs editing."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Editing existing booking
            # Service is already read-only, just ensure it's displayed
            fieldsets[0][1]['fields'] = ('booking_reference', 'customer', 'service', 'status')
        return fieldsets


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'status', 'cleaning_frequency', 'suburb', 'created_at')
    list_filter = ('status', 'cleaning_frequency', 'created_at')
    search_fields = ('customer__full_name', 'customer__email', 'suburb')
    readonly_fields = ('created_at', 'updated_at', 'service')
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
