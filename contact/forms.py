from django import forms
from .models import ContactMessage
import re
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+61 2 1234 5678'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone_digits = re.sub(r'\D', '', phone)
            if not (len(phone_digits) == 10 and phone_digits.startswith(('02', '03', '04', '07', '08'))):
                raise ValidationError("Please enter a valid Australian phone number.")
        return phone
