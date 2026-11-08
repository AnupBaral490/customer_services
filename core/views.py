from django.shortcuts import render
from django.views.generic import TemplateView
from services.models import Service
from .models import Testimonial, FAQ


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_services'] = Service.objects.filter(is_active=True)[:6]
        context['testimonials'] = Testimonial.objects.filter(is_approved=True)[:6]
        context['faqs'] = FAQ.objects.filter(is_active=True)[:8]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy-policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms-conditions.html'


class CancellationPolicyView(TemplateView):
    template_name = 'core/cancellation-policy.html'
