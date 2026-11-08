from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, QuoteRequest
from customers.models import Customer
import re


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['preferred_date', 'preferred_time', 'property_type', 'bedrooms', 'bathrooms', 'property_size', 'additional_requirements']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'property_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 100 sqm'}),
            'additional_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class BookingCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone', 'address', 'suburb', 'postcode']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+61 2 1234 5678'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'suburb': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic Australian phone validation
            phone_digits = re.sub(r'\D', '', phone)
            if not (len(phone_digits) == 10 and phone_digits.startswith(('02', '03', '04', '07', '08'))):
                raise ValidationError("Please enter a valid Australian phone number.")
        return phone


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['service', 'property_type', 'cleaning_frequency', 'suburb', 'postcode', 'additional_requirements']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'cleaning_frequency': forms.Select(attrs={'class': 'form-select'}),
            'suburb': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
            'additional_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class QuoteRequestCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+61 2 1234 5678'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone_digits = re.sub(r'\D', '', phone)
            if not (len(phone_digits) == 10 and phone_digits.startswith(('02', '03', '04', '07', '08'))):
                raise ValidationError("Please enter a valid Australian phone number.")
        return phone
