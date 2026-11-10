from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, QuoteRequest
from customers.models import Customer
import re


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'preferred_date', 'preferred_time', 'property_type', 'bedrooms', 'bathrooms', 'property_size', 'additional_requirements']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
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
            # Remove all non-digit characters
            phone_digits = re.sub(r'\D', '', phone)
            # Accept any phone number with at least 7 digits for testing
            if len(phone_digits) < 7:
                raise ValidationError("Please enter a valid phone number (at least 7 digits).")
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
            if len(phone_digits) not in [10, 11]:
                raise ValidationError("Please enter a valid Australian phone number (10 digits). Example: +61412345678 or 0412345678")
        return phone


class BookingCancellationForm(forms.Form):
    """Form for customers to cancel their bookings."""
    REASON_CHOICES = [
        ('schedule_conflict', 'Schedule Conflict'),
        ('no_longer_needed', 'No Longer Needed'),
        ('found_alternative', 'Found Alternative Service'),
        ('financial_reasons', 'Financial Reasons'),
        ('other', 'Other Reason'),
    ]
    
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Cancellation Reason',
        required=True
    )
    
    additional_details = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please provide any additional details (optional)'
        }),
        required=False,
        label='Additional Details'
    )
    
    confirm_cancellation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=True,
        label='I understand the cancellation policy and confirm my cancellation request'
    )
