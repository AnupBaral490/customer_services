from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'display_order', 'price', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'slug')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Details', {
            'fields': ('what_included', 'price', 'display_order')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )
