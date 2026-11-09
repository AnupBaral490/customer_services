from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('signup/', views.customer_signup, name='customer-signup'),
    path('login/', views.customer_login, name='customer-login'),
    path('logout/', views.customer_logout, name='customer-logout'),
    path('profile/', views.customer_profile, name='customer-profile'),
]
