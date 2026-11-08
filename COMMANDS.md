# Django Commands Reference

## Quick Command Reference

Set Python path before running commands:
```bash
# Windows
set PYTHONPATH=.

# Mac/Linux
export PYTHONPATH=.
```

---

## Development Server

### Start the server
```bash
# Windows
run.bat

# Mac/Linux
bash run.sh

# Manual
python config/manage.py runserver
python config/manage.py runserver 0.0.0.0:8000  # All interfaces
```

---

## Database Management

### Check database status
```bash
python config/manage.py check
```

### Create migrations (after model changes)
```bash
python config/manage.py makemigrations
python config/manage.py makemigrations [app_name]
```

### Apply migrations
```bash
python config/manage.py migrate
python config/manage.py migrate [app_name]
python config/manage.py migrate [app_name] [migration_number]
```

### Show migration status
```bash
python config/manage.py showmigrations
python config/manage.py showmigrations [app_name]
```

### Reverse migrations
```bash
python config/manage.py migrate [app_name] zero  # Remove all
python config/manage.py migrate [app_name] 0001  # Revert to specific
```

### Create empty migration
```bash
python config/manage.py makemigrations [app_name] --empty --name [description]
```

---

## Admin & User Management

### Create superuser
```bash
python config/manage.py createsuperuser
python config/manage.py createsuperuser --username admin --email admin@example.com
```

### Change password
```bash
python config/manage.py changepassword [username]
python config/manage.py changepassword admin
```

### Remove user
```bash
python config/manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='username').delete()
```

---

## Database Backup & Restore

### Export data (dump)
```bash
python config/manage.py dumpdata > backup.json
python config/manage.py dumpdata [app_name] > app_backup.json
python config/manage.py dumpdata [app_name].[model] > model_backup.json
```

Examples:
```bash
python config/manage.py dumpdata bookings > bookings.json
python config/manage.py dumpdata core.testimonial > testimonials.json
```

### Import data (load)
```bash
python config/manage.py loaddata backup.json
python config/manage.py loaddata app_backup.json
```

### Clear specific app data
```bash
python config/manage.py shell
>>> from [app_name].models import [Model]
>>> [Model].objects.all().delete()
```

---

## Django Shell

### Access Python shell with Django context
```bash
python config/manage.py shell
```

Once in shell:
```python
# List all services
from services.models import Service
Service.objects.all()

# Create a service
Service.objects.create(
    name="New Service",
    description="Description",
    what_included="Item 1, Item 2",
    price="From $99"
)

# Get specific service
service = Service.objects.get(name="Residential Cleaning")

# Update service
service.price = "From $119"
service.save()

# Delete service
service.delete()

# Filter services
active_services = Service.objects.filter(is_active=True)

# Count services
Service.objects.count()

# List all bookings
from bookings.models import Booking
Booking.objects.all()

# Get pending bookings
pending = Booking.objects.filter(status='pending')

# List all customers
from customers.models import Customer
Customer.objects.all()

# List all testimonials
from core.models import Testimonial
Testimonial.objects.filter(is_approved=True)

# Get all contact messages
from contact.models import ContactMessage
ContactMessage.objects.filter(is_read=False)
```

### Exit shell
```python
exit()
```

---

## Static Files

### Collect static files for production
```bash
python config/manage.py collectstatic --noinput
python config/manage.py collectstatic --clear --noinput
```

### Clear collected static files
```bash
python config/manage.py collectstatic --clear --noinput
```

---

## Testing

### Run all tests
```bash
python config/manage.py test
```

### Run tests for specific app
```bash
python config/manage.py test [app_name]
python config/manage.py test core
```

### Run specific test class
```bash
python config/manage.py test [app_name].tests.[TestClass]
```

### Run with verbose output
```bash
python config/manage.py test --verbosity=2
```

### Run and keep test database
```bash
python config/manage.py test --keepdb
```

---

## Code Quality

### Check for issues
```bash
python config/manage.py check
python config/manage.py check [app_name]
```

### Run linting (if flake8 installed)
```bash
flake8 .
flake8 [app_name]
```

### Format code (if black installed)
```bash
black .
black [app_name]
```

---

## URL Configuration

### Display all URL patterns
```bash
python config/manage.py show_urls
```

---

## Custom Scripts

### Create superuser (included)
```bash
python create_superuser.py
```

### Initialize sample data (included)
```bash
python init_sample_data.py
```

---

## Debugging

### Django Debug Toolbar (if installed)
Install:
```bash
pip install django-debug-toolbar
```

Add to INSTALLED_APPS in settings.py:
```python
'debug_toolbar',
```

### Python debugger
```python
import pdb; pdb.set_trace()  # In your code
```

### Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Message")
logger.info("Message")
logger.warning("Message")
logger.error("Message")
```

---

## Environment & Dependencies

### List installed packages
```bash
pip list
```

### Show specific package info
```bash
pip show django
```

### Update packages
```bash
pip install --upgrade -r requirements.txt
```

### Export current packages
```bash
pip freeze > requirements.txt
```

---

## File Management

### Generate SECRET_KEY for production
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

In shell:
```bash
python config/manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

---

## Useful Django Management Commands

### Compile messages (i18n)
```bash
python config/manage.py compilemessages
```

### Make messages (i18n)
```bash
python config/manage.py makemessages -l es
```

### Graph models (if django-extensions installed)
```bash
python config/manage.py graph_models -o models.png
```

### Timeline of all migrations
```bash
python config/manage.py showmigrations --plan
```

---

## Environment Variables

Set via .env file:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
BUSINESS_NAME=Your Company
BUSINESS_PHONE=+61 2 1234 5678
BUSINESS_EMAIL=hello@company.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Production Commands

### Prepare for production
```bash
python config/manage.py check --deploy
python config/manage.py collectstatic --noinput
python config/manage.py migrate --noinput
```

### Run with Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Run with uWSGI
```bash
uwsgi --http :8000 --wsgi-file config/wsgi.py --master --processes 4 --threads 2
```

---

## Useful Shortcuts

### Reload code in shell without restarting
```python
import importlib
import [module_name]
importlib.reload([module_name])
```

### Get object or 404
```python
from django.shortcuts import get_object_or_404
service = get_object_or_404(Service, slug='residential-cleaning')
```

### Paginate results
```python
from django.core.paginator import Paginator
services = Service.objects.all()
paginator = Paginator(services, 10)  # 10 per page
page = paginator.get_page(1)  # Get page 1
```

---

## Troubleshooting Commands

### Reset all migrations (DANGEROUS - dev only)
```bash
python config/manage.py migrate --fake [app_name] zero
python config/manage.py makemigrations [app_name]
python config/manage.py migrate [app_name]
```

### Clear all data (DANGEROUS - dev only)
```bash
python config/manage.py flush
```

### Check migrations status
```bash
python config/manage.py showmigrations --list
```

### Verify database
```bash
python config/manage.py dbshell
```

---

## App Management

### Create new app
```bash
python config/manage.py startapp [app_name]
```

### Create new project
```bash
django-admin startproject [project_name]
```

### List all apps
```bash
python config/manage.py shell
>>> from django.apps import apps
>>> [app.name for app in apps.get_app_configs()]
```

---

## Performance

### Profile view (if django-silk installed)
Install:
```bash
pip install django-silk
```

### Find slow queries
In settings.py:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

---

## Common Workflow

```bash
# 1. Start development
set PYTHONPATH=.
python config/manage.py runserver

# 2. Make model changes
# Edit models.py

# 3. Create and apply migrations
python config/manage.py makemigrations
python config/manage.py migrate

# 4. Test in shell
python config/manage.py shell
# Test your code

# 5. Access admin
# http://localhost:8000/admin

# 6. Commit changes
# git add .
# git commit -m "message"
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Start server | `python config/manage.py runserver` |
| Create migration | `python config/manage.py makemigrations` |
| Apply migration | `python config/manage.py migrate` |
| Create admin | `python config/manage.py createsuperuser` |
| Change password | `python config/manage.py changepassword admin` |
| Django shell | `python config/manage.py shell` |
| Backup data | `python config/manage.py dumpdata > backup.json` |
| Restore data | `python config/manage.py loaddata backup.json` |
| Collect static | `python config/manage.py collectstatic --noinput` |
| Check status | `python config/manage.py check` |
| Show URLs | `python config/manage.py show_urls` |

---

**Pro Tip**: Always prefix commands with `set PYTHONPATH=.` on Windows or `export PYTHONPATH=.` on Mac/Linux to ensure Django can find your apps!

