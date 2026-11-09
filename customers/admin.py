from django.contrib import admin
from .models import CustomerProfile, Customer


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Admin for CustomerProfile model."""
    list_display = ('user', 'phone', 'suburb', 'created_at')
    list_filter = ('created_at', 'suburb')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Info', {
            'fields': ('phone', 'address', 'suburb', 'postcode')
        }),
        ('Profile', {
            'fields': ('profile_picture',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for legacy Customer model."""
    list_display = ('full_name', 'email', 'phone', 'suburb', 'created_at')
    list_filter = ('created_at', 'suburb')
    search_fields = ('full_name', 'email', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'suburb', 'postcode')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
