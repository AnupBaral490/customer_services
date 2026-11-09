from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms/', views.TermsAndConditionsView.as_view(), name='terms-conditions'),
    path('cancellation/', views.CancellationPolicyView.as_view(), name='cancellation-policy'),
    path('testimonials/submit/', views.TestimonialCreateView.as_view(), name='testimonial-submit'),
    path('testimonials/success/', views.TestimonialSuccessView.as_view(), name='testimonial-success'),
    path('how-to-review/', views.HowToReviewView.as_view(), name='how-to-review'),
]
