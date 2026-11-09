#!/usr/bin/env python
"""
Script to create all cleaning services in the database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

django.setup()

from services.models import Service

# Services to create
services_data = [
    {
        'name': 'Pressure Washing',
        'description': 'Professional high-pressure washing for driveways, patios, decking, and exterior surfaces. We remove dirt, grime, and stubborn stains safely and effectively.',
        'what_included': 'Driveway cleaning, Patio/deck washing, Pathway cleaning, House exterior wash, Gutter cleaning',
        'price': 'From $150',
        'display_order': 1,
    },
    {
        'name': 'End of Lease Clean',
        'description': 'Comprehensive end of lease cleaning designed to help you get your full bond back. We detail every room to meet real estate standards.',
        'what_included': 'Full property detail clean, Carpet cleaning, Window washing, Bond cleaning guarantee, Real estate approved',
        'price': 'From $400',
        'display_order': 2,
    },
    {
        'name': 'Mould Clean',
        'description': 'Professional mould removal and prevention services. We safely eliminate mould, mildew, and moisture issues to improve air quality.',
        'what_included': 'Mould removal, Mildew treatment, Moisture assessment, Prevention recommendations, Non-toxic solutions',
        'price': 'From $200',
        'display_order': 3,
    },
    {
        'name': 'Builders Clean',
        'description': 'Post-construction cleaning for new builds, renovations, and major projects. We handle dust, debris, and construction residue thoroughly.',
        'what_included': 'Dust removal, Debris cleanup, Window cleaning, Floor finishing, Site inspection',
        'price': 'From $600',
        'display_order': 4,
    },
    {
        'name': 'Office and Commercial Cleaning',
        'description': 'Professional commercial cleaning services for offices, retail spaces, and businesses. Maintain a clean, healthy workspace for employees and clients.',
        'what_included': 'Office cleaning, Bathroom sanitization, Kitchen areas, Carpet care, Trash removal, Daily or weekly schedules',
        'price': 'Custom quote',
        'display_order': 5,
    },
    {
        'name': 'Regular Weekly and Fortnightly Clean',
        'description': 'Consistent residential cleaning on your preferred schedule. Keep your home fresh and organized with our reliable weekly or fortnightly service.',
        'what_included': 'Regular home cleaning, Dusting, Vacuuming, Bathroom cleaning, Kitchen cleaning, Flexible scheduling',
        'price': 'From $120 weekly',
        'display_order': 6,
    },
    {
        'name': 'Carpet Cleaning',
        'description': 'Professional deep carpet cleaning using latest equipment and eco-friendly solutions. Revive your carpets and extend their lifespan.',
        'what_included': 'Deep carpet clean, Stain removal, Carpet deodorizing, Upholstery cleaning, Quick drying process',
        'price': 'From $180',
        'display_order': 7,
    },
    {
        'name': 'Glass/Window Clean',
        'description': 'Crystal clear windows and glass surfaces. We clean windows, glass doors, and mirrors for a spotless finish inside and out.',
        'what_included': 'Internal window cleaning, External window cleaning, Glass door cleaning, Mirror cleaning, Frame dusting',
        'price': 'From $100',
        'display_order': 8,
    },
    {
        'name': 'General House Clean',
        'description': 'Thorough general house cleaning covering all rooms. Perfect for busy households looking for a comprehensive clean.',
        'what_included': 'All rooms cleaning, Bathroom sanitization, Kitchen deep clean, Dusting, Vacuuming, Mopping',
        'price': 'From $200',
        'display_order': 9,
    },
    {
        'name': 'NDIS Cleaning',
        'description': 'Specialized cleaning services for NDIS participants. We understand the importance of clean, safe living spaces and provide compassionate service.',
        'what_included': 'NDIS-approved cleaning, Flexible scheduling, Respectful service, Detailed reporting, Budget management',
        'price': 'From $180',
        'display_order': 10,
    },
    {
        'name': 'Lawn Mowing and Garden Maintenance',
        'description': 'Keep your outdoor spaces pristine with professional lawn mowing and garden maintenance. Regular upkeep for a beautiful property.',
        'what_included': 'Lawn mowing, Garden tidying, Weed control, Hedge trimming, Leaf removal, Seasonal maintenance',
        'price': 'From $80',
        'display_order': 11,
    },
]

def create_services():
    """Create all services in the database."""
    created_count = 0
    updated_count = 0
    
    for service_data in services_data:
        service, created = Service.objects.update_or_create(
            name=service_data['name'],
            defaults={
                'description': service_data['description'],
                'what_included': service_data['what_included'],
                'price': service_data['price'],
                'display_order': service_data['display_order'],
                'is_active': True,
            }
        )
        
        if created:
            created_count += 1
            print(f'✓ Created: {service.name}')
        else:
            updated_count += 1
            print(f'⟳ Updated: {service.name}')
    
    print(f'\n✓ Total Created: {created_count}')
    print(f'⟳ Total Updated: {updated_count}')
    print(f'✓ All services ready!')

if __name__ == '__main__':
    create_services()
