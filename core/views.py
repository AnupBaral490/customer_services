from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from services.models import Service
from .models import Testimonial, FAQ
from .forms import TestimonialForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_services'] = Service.objects.filter(is_active=True)[:6]
        context['testimonials'] = Testimonial.objects.filter(is_approved=True)[:6]
        context['faqs'] = FAQ.objects.filter(is_active=True)[:8]
        return context


class TestimonialCreateView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'core/submit-testimonial.html'
    success_url = reverse_lazy('core:testimonial-success')

    def form_valid(self, form):
        form.instance.user = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)


class TestimonialSuccessView(TemplateView):
    template_name = 'core/testimonial-success.html'


class HowToReviewView(TemplateView):
    template_name = 'core/how-to-review.html'


class AboutView(TemplateView):
    template_name = 'core/about.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy-policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms-conditions.html'


class CancellationPolicyView(TemplateView):
    template_name = 'core/cancellation-policy.html'
