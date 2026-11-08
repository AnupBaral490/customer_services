from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bookings/', views.bookings_list, name='bookings-list'),
    path('quotes/', views.quotes_list, name='quotes-list'),
    path('messages/', views.messages_list, name='messages-list'),
]
