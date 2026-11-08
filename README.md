# Premium Cleaning Services Website

A professional, production-ready Django website for an Australian cleaning services company.

## Features

- **Professional Design**: Modern, responsive Bootstrap 5 interface
- **Service Management**: Display and manage cleaning services
- **Booking System**: Customers can request bookings with service confirmation
- **Quote Requests**: Get free quote requests from customers
- **Customer Management**: Track customers and their interactions
- **Contact Management**: Handle and respond to customer inquiries
- **Admin Dashboard**: Custom admin dashboard for business management
- **Email Notifications**: Automated email confirmations
- **Australian Localization**: DD/MM/YYYY dates, Australian phone numbers, AUD currency ready

## Tech Stack

- **Backend**: Django 4.2.8
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Image Handling**: Pillow
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation

### 1. Clone and Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create a .env file
cp .env.example .env

# Edit .env with your settings
```

### 2. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
cleaning_services/
├── config/              # Django settings and URLs
├── core/                # Home, about, FAQs, testimonials
├── services/            # Service listings and details
├── bookings/            # Booking and quote requests
├── customers/           # Customer information
├── contact/             # Contact forms and messages
├── dashboard/           # Admin dashboard
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # User-uploaded content
├── manage.py
└── requirements.txt
```

## Admin Panel

Access the admin panel at `/admin/` with your superuser credentials to:

- Manage services
- View and confirm bookings
- Review quote requests
- Approve testimonials
- Manage FAQs
- View customer information
- Handle contact messages

## Configuration

Edit `config/settings.py` or set environment variables in `.env`:

- `BUSINESS_NAME`: Your company name
- `BUSINESS_PHONE`: Customer support phone
- `BUSINESS_EMAIL`: Support email address
- `BUSINESS_ADDRESS`: Business address
- `WHATSAPP_NUMBER`: WhatsApp contact number (without +)
- `EMAIL_HOST_USER`: SMTP email for sending messages

## Database Models

### Core
- **Testimonial**: Customer reviews and ratings
- **FAQ**: Frequently asked questions

### Services
- **Service**: Cleaning service offerings

### Bookings
- **Booking**: Customer booking requests
- **QuoteRequest**: Customer quote requests

### Customers
- **Customer**: Customer information

### Contact
- **ContactMessage**: Customer inquiries

## Emails

The system automatically sends:

- Booking confirmation to customers
- Quote request acknowledgment
- Contact form confirmation

Configure your email provider in `.env` (Gmail, Outlook, etc.)

## Security

- CSRF protection enabled
- Secure form handling
- Input validation on all forms
- Australian phone number validation
- Email validation
- Production settings for HTTPS and secure cookies

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Generate a new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Switch to PostgreSQL database
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up HTTPS with SSL certificates
7. Configure email service
8. Run `python manage.py collectstatic`

## Customization

### Adding Services

1. Go to Django admin (`/admin/`)
2. Click "Add Service"
3. Fill in details, upload image
4. Service appears on website immediately

### Modifying Pages

Edit templates in `templates/` folder:
- `core/home.html` - Homepage
- `core/about.html` - About page
- `contact/contact.html` - Contact page

### Styling

Customize colors in `static/css/style.css`:
```css
:root {
    --primary: #183D39;
    --secondary: #DCEFE8;
    --accent: #DCA85C;
}
```

## Legal Pages

Update these templates with your specific terms:
- `templates/core/privacy-policy.html`
- `templates/core/terms-conditions.html`
- `templates/core/cancellation-policy.html`

⚠️ **Note**: Have these reviewed by a legal professional for Australian compliance.

## Support

For issues or questions:
- Contact: {{ BUSINESS_EMAIL }}
- Phone: {{ BUSINESS_PHONE }}

## License

This website is custom-developed for your business.

---

**Last Updated**: November 2024
