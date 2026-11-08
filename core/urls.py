from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms/', views.TermsAndConditionsView.as_view(), name='terms-conditions'),
    path('cancellation/', views.CancellationPolicyView.as_view(), name='cancellation-policy'),
]
