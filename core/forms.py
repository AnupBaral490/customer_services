from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['customer_name', 'service', 'rating', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'service': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service You Used (e.g., Residential Cleaning)',
                'required': True,
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'rating-input',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with us...',
                'rows': 5,
                'required': True,
            }),
        }
        labels = {
            'customer_name': 'Full Name',
            'service': 'Service',
            'rating': 'Rating',
            'comment': 'Your Review',
        }
