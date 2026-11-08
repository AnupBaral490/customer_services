#!/usr/bin/env python
"""Create a superuser for the admin panel."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '.')
sys.path.insert(0, 'config')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")
    print("Change this password immediately in production!")
else:
    print("Superuser 'admin' already exists")
