# Premium Australian Cleaning Services Website - Setup Guide

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your settings
cp .env.example .env
# Edit .env with your business information
```

### 2. Initialize Database

The database is already set up with migrations. Just verify:

```bash
# From project root
set PYTHONPATH=.
python config/manage.py check
```

### 3. Create Admin User

A default admin user was created during setup:
- **Username**: admin
- **Password**: admin123

⚠️ **IMPORTANT**: Change this password immediately after first login!

```bash
set PYTHONPATH=.
python config/manage.py changepassword admin
```

### 4. Run Development Server

**On Windows:**
```bash
run.bat
```

**On Mac/Linux:**
```bash
bash run.sh
```

**Or manually:**
```bash
set PYTHONPATH=.
cd config
python manage.py runserver
```

Visit: http://localhost:8000

## Project Features

✅ **Homepage** - Hero section, services overview, testimonials, FAQs, CTA  
✅ **Services** - Manage services with images, pricing, and details  
✅ **Booking System** - Customers request bookings with auto-confirmation emails  
✅ **Quote Requests** - Generate personalized quotes  
✅ **Contact Forms** - Handle customer inquiries  
✅ **Admin Dashboard** - View statistics and manage bookings  
✅ **Customer Management** - Track all customer interactions  
✅ **Responsive Design** - Mobile-first Bootstrap 5 interface  
✅ **Australian Localization** - DD/MM/YYYY dates, phone validation  
✅ **Email Notifications** - Automated confirmations and alerts  

## Admin Panel

Access at: http://localhost:8000/admin/

Use your admin credentials to:
- ➕ Add/edit services
- ✅ Approve/confirm bookings
- 📝 Manage quote requests
- ⭐ Approve customer testimonials
- ❓ Create FAQ entries
- 👥 View customer information
- 📧 Manage contact messages

## Customization Guide

### 1. Add Services

1. Go to Admin Panel → Services → Add Service
2. Fill in:
   - **Name**: Service name
   - **Description**: Full description
   - **What's Included**: Comma-separated list
   - **Price**: e.g., "From $99"
   - **Image**: Upload service photo
   - **Active**: Enable service

### 2. Edit Business Information

Edit `.env` file:
```env
BUSINESS_NAME=Your Company Name
BUSINESS_PHONE=+61 2 XXXX XXXX
BUSINESS_EMAIL=hello@yoursite.com.au
BUSINESS_ADDRESS=Your Address, NSW 2000
WHATSAPP_NUMBER=61412345678
```

### 3. Customize Colors

Edit `static/css/style.css`:
```css
:root {
    --primary: #183D39;           /* Main brand color */
    --secondary: #DCEFE8;         /* Secondary color */
    --accent: #DCA85C;            /* Accent color */
    --text: #252B2A;              /* Text color */
}
```

### 4. Update Legal Pages

Edit templates:
- `templates/core/privacy-policy.html`
- `templates/core/terms-conditions.html`
- `templates/core/cancellation-policy.html`

⚠️ **Have these reviewed by a legal professional for Australian compliance**

### 5. Setup Email Notifications

For Gmail:
1. Enable "Less secure app access" or use App Password
2. Edit `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Project Structure

```
cleaning_services/
├── config/                 # Django settings & URLs
│   ├── config/
│   │   ├── settings.py    # Main settings
│   │   ├── urls.py        # URL routes
│   │   └── ...
│   └── manage.py          # Django CLI
├── core/                   # Homepage, About, FAQs
├── services/               # Service listings
├── bookings/               # Booking & quote requests
├── customers/              # Customer data
├── contact/                # Contact forms
├── dashboard/              # Admin dashboard
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements.txt        # Dependencies
└── README.md              # Project documentation
```

## Database Models

### Service
- name, slug, description, what_included, image, price, is_active

### Customer
- full_name, email, phone, address, suburb, postcode

### Booking
- booking_reference, customer, service, property_type, bedrooms, bathrooms, property_size, preferred_date, preferred_time, additional_requirements, status, internal_notes, assigned_staff

### QuoteRequest
- customer, service, property_type, cleaning_frequency, suburb, postcode, additional_requirements, status, estimated_quote

### ContactMessage
- full_name, email, phone, subject, message, is_read

### Testimonial
- customer_name, service, rating, comment, is_approved

### FAQ
- question, answer, is_active, display_order

## URLs Reference

| Page | URL |
|------|-----|
| Home | `/` |
| Services | `/services/` |
| Service Detail | `/services/[slug]/` |
| About | `/about/` |
| Book Cleaning | `/bookings/booking/` |
| Get Quote | `/bookings/quote/` |
| Contact | `/contact/` |
| Admin | `/admin/` |
| Dashboard | `/dashboard/` |
| Privacy | `/privacy/` |
| Terms | `/terms/` |
| Cancellation | `/cancellation/` |

## Production Deployment

Before deploying:

1. **Security**
   - Set `DEBUG=False` in `.env`
   - Generate a new SECRET_KEY
   - Set appropriate ALLOWED_HOSTS
   - Use HTTPS only

2. **Database**
   - Switch to PostgreSQL
   - Run migrations on production

3. **Email**
   - Configure production email service
   - Set up email domain authentication

4. **Static Files**
   ```bash
   python config/manage.py collectstatic --noinput
   ```

5. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx reverse proxy

## Common Tasks

### Create New Service
```bash
set PYTHONPATH=.
python config/manage.py shell
>>> from services.models import Service
>>> Service.objects.create(
...     name="New Service",
...     description="Description",
...     what_included="Item 1, Item 2",
...     price="From $99",
...     is_active=True
... )
```

### Export Data
```bash
set PYTHONPATH=.
python config/manage.py dumpdata bookings > bookings.json
python config/manage.py loaddata bookings.json
```

### Create Backup
```bash
set PYTHONPATH=.
python config/manage.py dumpdata > backup.json
```

## Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'config'"
```bash
set PYTHONPATH=.
python config/manage.py runserver
```

**Issue**: Database errors
```bash
set PYTHONPATH=.
python config/manage.py migrate --run-syncdb
```

**Issue**: Static files not loading
```bash
set PYTHONPATH=.
python config/manage.py collectstatic --noinput
```

**Issue**: Admin panel not working
```bash
set PYTHONPATH=.
python config/manage.py changepassword admin
```

## Support

For issues or questions:
- Review Django documentation: https://docs.djangoproject.com/
- Check Bootstrap 5 docs: https://getbootstrap.com/
- Review your settings: `config/config/settings.py`

---

**Project Created**: November 2024  
**Django Version**: 4.2.8  
**Bootstrap Version**: 5.3  
**Status**: Production Ready ✅
