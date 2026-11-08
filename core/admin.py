from django.contrib import admin
from .models import Testimonial, FAQ


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('customer_name', 'service', 'comment')
    readonly_fields = ('created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('display_order', 'created_at')
    readonly_fields = ('created_at',)
