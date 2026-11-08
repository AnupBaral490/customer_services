from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactPageView.as_view(), name='contact'),
    path('message/', views.contact_message_view, name='message'),
    path('success/', views.contact_success, name='contact-success'),
]
