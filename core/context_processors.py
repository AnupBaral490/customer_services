from django.conf import settings
from services.models import Service


def business_info(request):
    """Make business information and services available in all templates."""
    return {
        'BUSINESS_NAME': settings.BUSINESS_NAME,
        'BUSINESS_PHONE': settings.BUSINESS_PHONE,
        'BUSINESS_EMAIL': settings.BUSINESS_EMAIL,
        'BUSINESS_ADDRESS': settings.BUSINESS_ADDRESS,
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'services': Service.objects.filter(is_active=True).order_by('display_order')[:3],
    }
