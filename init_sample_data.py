#!/usr/bin/env python
"""Initialize sample data for the cleaning services website."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '.')
sys.path.insert(0, 'config')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import Service
from core.models import Testimonial, FAQ

# Create sample services
services_data = [
    {
        'name': 'Residential Cleaning',
        'description': 'Professional cleaning for your home, including all rooms, kitchens, bathrooms, and living areas.',
        'what_included': 'Dusting, Vacuuming, Mopping, Kitchen Cleaning, Bathroom Cleaning, Trash Removal',
        'price': 'From $89',
        'display_order': 1,
    },
    {
        'name': 'Commercial Cleaning',
        'description': 'Keep your office and workspace clean and professional with our commercial cleaning services.',
        'what_included': 'Floor Cleaning, Restroom Sanitizing, Trash Removal, Surface Disinfection, Glass Cleaning',
        'price': 'Custom Quote',
        'display_order': 2,
    },
    {
        'name': 'Office Cleaning',
        'description': 'Daily or weekly office cleaning to maintain a productive and healthy work environment.',
        'what_included': 'Desk Cleaning, Floor Cleaning, Restroom Cleaning, Window Cleaning, Carpet Vacuuming',
        'price': 'Custom Quote',
        'display_order': 3,
    },
    {
        'name': 'Deep Cleaning',
        'description': 'Thorough cleaning of every corner, including baseboards, ceiling fans, and tight spaces.',
        'what_included': 'Baseboards, Ceiling Fans, Behind Appliances, Carpet Shampooing, Wall Washing',
        'price': 'From $249',
        'display_order': 4,
    },
    {
        'name': 'End-of-Lease Cleaning',
        'description': 'Get your full bond back with our comprehensive end-of-lease cleaning service.',
        'what_included': 'Deep Carpet Clean, Wall Washing, Appliance Cleaning, Window Cleaning, Bond Guarantee',
        'price': 'From $349',
        'display_order': 5,
    },
    {
        'name': 'Carpet Cleaning',
        'description': 'Professional carpet cleaning using eco-friendly methods that remove dirt and stains.',
        'what_included': 'Hot Water Extraction, Spot Treatment, Deodorizing, Fast Drying',
        'price': 'From $149',
        'display_order': 6,
    },
]

# Create sample testimonials
testimonials_data = [
    {
        'customer_name': 'Sarah Johnson',
        'service': 'Residential Cleaning',
        'rating': 5,
        'comment': 'Absolutely fantastic service! The team was professional, punctual, and left my home spotless. Highly recommend!',
        'is_approved': True,
    },
    {
        'customer_name': 'Michael Chen',
        'service': 'Commercial Cleaning',
        'rating': 5,
        'comment': 'Outstanding quality and reliability. They keep our office immaculate. Best cleaning service in Sydney!',
        'is_approved': True,
    },
    {
        'customer_name': 'Emma Wilson',
        'service': 'End-of-Lease Cleaning',
        'rating': 5,
        'comment': 'Got my full bond back thanks to their thorough end-of-lease cleaning. Worth every penny!',
        'is_approved': True,
    },
]

# Create sample FAQs
faqs_data = [
    {
        'question': 'How long does a typical cleaning take?',
        'answer': 'The time depends on the property size and type of cleaning. A standard residential clean typically takes 2-4 hours.',
        'is_active': True,
        'display_order': 1,
    },
    {
        'question': 'Do you provide your own cleaning supplies?',
        'answer': 'Yes, we bring all our eco-friendly cleaning supplies. However, you can request specific products if needed.',
        'is_active': True,
        'display_order': 2,
    },
    {
        'question': 'Can I reschedule my cleaning appointment?',
        'answer': 'Yes, you can reschedule up to 3 days before your appointment at no charge. Please contact us for details.',
        'is_active': True,
        'display_order': 3,
    },
    {
        'question': 'What is your cancellation policy?',
        'answer': 'We offer full refunds for cancellations made 7+ days before. See our cancellation policy for details.',
        'is_active': True,
        'display_order': 4,
    },
    {
        'question': 'Are your staff insured and background checked?',
        'answer': 'Yes, all our team members are fully insured, background checked, and professionally trained.',
        'is_active': True,
        'display_order': 5,
    },
    {
        'question': 'Do you offer a satisfaction guarantee?',
        'answer': 'Absolutely! If you\'re not satisfied, we\'ll re-clean at no charge. Your satisfaction is guaranteed.',
        'is_active': True,
        'display_order': 6,
    },
]

def init_data():
    """Create sample data if it doesn't exist."""
    print("Initializing sample data...")
    
    # Create services
    print("\nCreating services...")
    for data in services_data:
        service, created = Service.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'what_included': data['what_included'],
                'price': data['price'],
                'display_order': data['display_order'],
                'is_active': True,
            }
        )
        if created:
            print(f"  ✓ Created: {data['name']}")
        else:
            print(f"  • Already exists: {data['name']}")
    
    # Create testimonials
    print("\nCreating testimonials...")
    for data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            customer_name=data['customer_name'],
            service=data['service'],
            defaults={
                'rating': data['rating'],
                'comment': data['comment'],
                'is_approved': data['is_approved'],
            }
        )
        if created:
            print(f"  ✓ Created: {data['customer_name']}'s testimonial")
        else:
            print(f"  • Already exists: {data['customer_name']}'s testimonial")
    
    # Create FAQs
    print("\nCreating FAQs...")
    for data in faqs_data:
        faq, created = FAQ.objects.get_or_create(
            question=data['question'],
            defaults={
                'answer': data['answer'],
                'is_active': data['is_active'],
                'display_order': data['display_order'],
            }
        )
        if created:
            print(f"  ✓ Created: FAQ #{data['display_order']}")
        else:
            print(f"  • Already exists: FAQ #{data['display_order']}")
    
    print("\n✅ Sample data initialization complete!")
    print("\nYou can now:")
    print("  • Visit http://localhost:8000 to see your website")
    print("  • Go to http://localhost:8000/admin to manage content")
    print("  • Edit services, add testimonials, and manage bookings")

if __name__ == '__main__':
    init_data()
