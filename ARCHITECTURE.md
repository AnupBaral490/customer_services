# System Architecture Overview

## 🏗️ Application Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USERS / BROWSERS                   │
│         (Customers visiting the website)             │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/HTTPS
                     ↓
┌─────────────────────────────────────────────────────┐
│              DJANGO WEB APPLICATION                  │
│  (Port 8000 - Development, Gunicorn - Production)  │
├─────────────────────────────────────────────────────┤
│  URL ROUTER (config/urls.py)                        │
│  ├─ / (core.urls)                                  │
│  ├─ /services/ (services.urls)                     │
│  ├─ /bookings/ (bookings.urls)                     │
│  ├─ /contact/ (contact.urls)                       │
│  ├─ /dashboard/ (dashboard.urls)                   │
│  └─ /admin/ (Django admin)                         │
└────────────────────────────────────────────────────┘
         │              │              │
         ↓              ↓              ↓
    ┌────────┐   ┌──────────┐   ┌──────────┐
    │ VIEWS  │   │  FORMS   │   │ TEMPLATES│
    ├────────┤   ├──────────┤   ├──────────┤
    │ core   │   │BookingForm    │base.html │
    │services│   │QuoteForm      │home.html │
    │bookings│   │ContactForm    │services/ │
    │contact │   │             │bookings/ │
    │dashboard   │             │contact/ │
    └────────┘   └──────────┘   └──────────┘
         │              │              │
         └──────────────┼──────────────┘
                       ↓
         ┌─────────────────────────────┐
         │     DJANGO ORM MODELS       │
         ├─────────────────────────────┤
         │ Service                     │
         │ Booking  ──────┐            │
         │ QuoteRequest   │            │
         │ Customer ──────┼──────┐    │
         │ ContactMessage │      │    │
         │ Testimonial ───┼──────┤    │
         │ FAQ            │      │    │
         └────────┬─────────────┬────┘
                  ↓             ↓
         ┌─────────────────────────────┐
         │    SQLite DATABASE          │
         │ (db.sqlite3)               │
         │                            │
         │ Tables:                    │
         │ • services_service         │
         │ • bookings_booking         │
         │ • bookings_quoterequest    │
         │ • customers_customer       │
         │ • contact_contactmessage   │
         │ • core_testimonial         │
         │ • core_faq                 │
         │ • auth_user (admin)        │
         └─────────────────────────────┘
```

---

## 🔄 User Journey: Booking a Service

```
1. CUSTOMER VISITS WEBSITE
   ↓
2. VIEWS HOME PAGE
   ├─ See services
   ├─ Read testimonials
   ├─ Check FAQs
   ↓
3. CLICKS "BOOK NOW"
   ↓
4. FILLS BOOKING FORM
   ├─ Personal info (name, email, phone)
   ├─ Service selection
   ├─ Property details
   ├─ Date & time
   ↓
5. SUBMITS FORM
   ├─ Django validates input
   ├─ Creates Customer record (if new)
   ├─ Creates Booking record
   ├─ Generates booking reference
   ↓
6. EMAIL CONFIRMATION SENT
   ├─ To customer
   ├─ Contains booking reference
   ├─ Contains service details
   ↓
7. ADMIN NOTIFIED
   ├─ Dashboard shows new booking
   ├─ Status: "Pending"
   ↓
8. ADMIN CONFIRMS BOOKING
   ├─ Updates status: "Confirmed"
   ├─ Customer receives confirmation email
   ↓
9. CLEANING DAY ARRIVES
   ├─ Team performs cleaning
   ↓
10. ADMIN MARKS COMPLETE
    ├─ Updates status: "Completed"
    ├─ Optionally request testimonial
```

---

## 💾 Database Schema Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    SERVICE DATABASE                       │
├──────────────────────────────────────────────────────────┤

SERVICES TABLE
├─ id (PK)
├─ name
├─ slug (unique)
├─ description
├─ what_included
├─ image (path)
├─ price
├─ is_active
├─ display_order
└─ created_at

                         ↓ (FK)

CUSTOMERS TABLE
├─ id (PK)
├─ full_name
├─ email
├─ phone
├─ address
├─ suburb
├─ postcode
└─ created_at

    ↓ (FK)               ↓ (FK)
BOOKINGS TABLE       QUOTEREQUEST TABLE
├─ id (PK)          ├─ id (PK)
├─ booking_ref      ├─ customer_id (FK)
├─ customer_id (FK) ├─ service_id (FK)
├─ service_id (FK)  ├─ property_type
├─ property_type    ├─ cleaning_freq
├─ bedrooms         ├─ suburb
├─ bathrooms        ├─ postcode
├─ property_size    ├─ status
├─ preferred_date   ├─ estimated_quote
├─ preferred_time   ├─ created_at
├─ status           └─ updated_at
├─ internal_notes
├─ assigned_staff
├─ created_at
└─ updated_at

CONTACT_MESSAGES TABLE
├─ id (PK)
├─ full_name
├─ email
├─ phone
├─ subject
├─ message
├─ is_read
└─ created_at

TESTIMONIALS TABLE
├─ id (PK)
├─ customer_name
├─ service
├─ rating (1-5)
├─ comment
├─ is_approved
└─ created_at

FAQ TABLE
├─ id (PK)
├─ question
├─ answer
├─ is_active
├─ display_order
└─ created_at

AUTH_USER TABLE (Django)
├─ id (PK)
├─ username
├─ email
├─ password_hash
├─ is_staff
├─ is_superuser
└─ ...
```

---

## 📱 Frontend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   BASE TEMPLATE (base.html)             │
│  ┌─────────────────────────────────────────────────┐   │
│  │ HTML5 Boilerplate                              │   │
│  │ ├─ Meta tags (SEO)                            │   │
│  │ ├─ Bootstrap 5 CSS                            │   │
│  │ ├─ Font Awesome icons                         │   │
│  │ └─ Custom CSS (static/css/style.css)          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ NAVIGATION BAR (includes/navbar.html)          │   │
│  │ ├─ Logo / Brand                               │   │
│  │ ├─ Menu links                                 │   │
│  │ └─ Book Now button                            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ MAIN CONTENT (extends base.html)               │   │
│  │ ├─ core/home.html                            │   │
│  │ ├─ services/service-list.html                 │   │
│  │ ├─ bookings/booking-form.html                 │   │
│  │ ├─ contact/contact.html                       │   │
│  │ └─ ... (other templates)                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ FOOTER (includes/footer.html)                  │   │
│  │ ├─ Company info                               │   │
│  │ ├─ Quick links                                │   │
│  │ ├─ Contact info                               │   │
│  │ └─ Legal links                                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ SCRIPTS                                         │   │
│  │ ├─ Bootstrap 5 JS                             │   │
│  │ └─ Custom JS (static/js/main.js)              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

CSS STYLING LAYERS:
├─ Bootstrap 5 (responsive grid, components)
├─ Custom CSS (colors, brand, custom components)
└─ Inline styles (dynamic content)

COLOR SCHEME:
├─ Primary: #183D39 (brand color)
├─ Secondary: #DCEFE8 (accent background)
├─ Accent: #DCA85C (highlights)
├─ Text: #252B2A (dark)
└─ Background: #F7F9F8 (light)
```

---

## 🔐 Authentication & Authorization

```
┌──────────────────────────────────────┐
│       DJANGO AUTHENTICATION          │
├──────────────────────────────────────┤

PUBLIC ACCESS (No login required):
├─ /                         (Home)
├─ /services/               (Service list)
├─ /services/[slug]/        (Service detail)
├─ /about/                  (About page)
├─ /bookings/booking/       (Booking form)
├─ /bookings/quote/         (Quote form)
├─ /contact/                (Contact page)
└─ /contact/message/        (Contact form)

AUTHENTICATED ACCESS (Staff only):
├─ /admin/                  (Django admin)
└─ /dashboard/              (Admin dashboard)

PERMISSION LEVELS:
├─ Superuser: Full access
├─ Staff: Limited access
├─ Anonymous: Public pages only
└─ Customers: Self-service booking

LOGIN REQUIRED:
@login_required(login_url='admin:login')
def dashboard(request):
    # Admin-only view
```

---

## 📧 Email System Flow

```
BOOKING CREATED
    ↓
DJANGO SENDS EMAILS
    ├─ To Customer: Confirmation
    │  ├─ Booking reference
    │  ├─ Service details
    │  ├─ Date & time
    │  └─ Next steps
    │
    └─ To Admin: Notification
       ├─ Customer details
       ├─ Booking details
       └─ Link to admin panel

QUOTE CREATED
    ↓
    ├─ To Customer: Quote request received
    │  ├─ Expected response time
    │  └─ Contact info
    │
    └─ To Admin: New quote request
       ├─ Customer details
       └─ Property requirements

CONTACT MESSAGE SUBMITTED
    ↓
    ├─ To Customer: Thank you confirmation
    │  └─ We'll respond soon
    │
    └─ To Admin: New message alert
       ├─ Full message details
       └─ Customer contact info

EMAIL CONFIGURATION:
Email Backend: SMTP (configurable)
Provider: Gmail, SendGrid, Amazon SES, etc.
Configuration: .env file
├─ EMAIL_HOST (smtp.gmail.com)
├─ EMAIL_PORT (587)
├─ EMAIL_HOST_USER (your-email@gmail.com)
└─ EMAIL_HOST_PASSWORD (app-password)
```

---

## 🚀 Request/Response Flow

```
USER REQUEST
    ↓
DJANGO URL ROUTER (urls.py)
    ├─ Matches URL pattern
    ├─ Resolves to view function/class
    └─ Passes parameters
    ↓
VIEW LAYER (views.py)
    ├─ Process request
    ├─ Validate input
    ├─ Query database (ORM)
    ├─ Prepare context
    └─ Render template
    ↓
MODEL LAYER (models.py)
    ├─ Query database
    ├─ Validate data
    ├─ Apply business logic
    └─ Return results
    ↓
TEMPLATE LAYER (templates/)
    ├─ Receive context data
    ├─ Render HTML
    ├─ Include static assets
    └─ Return to browser
    ↓
BROWSER RENDERS
    ├─ HTML structure
    ├─ CSS styling
    ├─ JavaScript execution
    └─ Display to user
```

---

## 🔄 MVC/MTV Pattern

```
Django follows MTV (Model-Template-View) pattern:

MODEL (models.py)
├─ Defines database structure
├─ Contains business logic
├─ Validates data
└─ Example: class Booking(models.Model)

TEMPLATE (templates/)
├─ HTML with Django tags
├─ Displays data
├─ User interface
└─ Example: booking-form.html

VIEW (views.py)
├─ Processes requests
├─ Queries models
├─ Renders templates
└─ Example: class BookingCreateView

URL Router (urls.py)
├─ Maps URLs to views
├─ Configuration
└─ Example: path('booking/', BookingCreateView.as_view())

REQUEST FLOW:
URL → View → Model → Template → Response
```

---

## 📊 Deployment Architecture (Production)

```
┌──────────────────────────────────────────────────────┐
│                   INTERNET / USERS                   │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓ (HTTPS)
        ┌────────────────────────────┐
        │     SSL/TLS CERTIFICATE    │
        │  (HTTPS encryption)        │
        └────────────────┬───────────┘
                        │
                        ↓
        ┌────────────────────────────┐
        │    REVERSE PROXY (Nginx)   │
        │  • Load balancing         │
        │  • Static file serving    │
        │  • Compression            │
        │  • Caching               │
        └────────────────┬───────────┘
                        │
                        ↓
        ┌────────────────────────────┐
        │  APPLICATION SERVER        │
        │  (Gunicorn / uWSGI)        │
        │  • 4+ worker processes    │
        │  • Request handling       │
        │  • Django application     │
        └────────────────┬───────────┘
                        │
                        ↓
        ┌────────────────────────────┐
        │    POSTGRESQL DATABASE     │
        │  (Replicated & backed up)  │
        │  • Primary DB             │
        │  • Backup replicas        │
        │  • Automated backups      │
        └────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────┐
        │    STATIC FILE STORAGE     │
        │  (AWS S3 / CDN)           │
        │  • CSS, JS, images        │
        │  • Media uploads          │
        └────────────────────────────┘
                        │
                        ↓
        ┌────────────────────────────┐
        │    EMAIL SERVICE           │
        │  (SendGrid / AWS SES)     │
        │  • Send confirmations     │
        │  • Send notifications     │
        └────────────────────────────┘
```

---

## 🔄 Data Flow: Booking Request

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Customer fills booking form                         │
├─────────────────────────────────────────────────────────────┤
│ Form inputs:                                                │
│ • full_name, email, phone, address, suburb, postcode      │
│ • service, property_type, bedrooms, bathrooms             │
│ • property_size, preferred_date, preferred_time            │
│ • additional_requirements                                  │
└─────────────┬───────────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Django validates form                              │
├─────────────────────────────────────────────────────────────┤
│ Validations:                                                │
│ ✓ Phone number format (Australian)                         │
│ ✓ Email format                                             │
│ ✓ Date in future                                           │
│ ✓ All required fields present                              │
│ ✓ CSRF token valid                                         │
└─────────────┬───────────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Save to database                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. Get or create Customer                                  │
│    └─ Query Customer by email                              │
│    └─ If not found, create new record                      │
│                                                            │
│ 2. Create Booking                                          │
│    └─ Generate booking_reference (auto)                    │
│    └─ Set status = "pending"                              │
│    └─ Save all data                                        │
│                                                            │
│ 3. Commit transaction                                      │
└─────────────┬───────────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Send confirmation emails                           │
├─────────────────────────────────────────────────────────────┤
│ Email 1 (Customer confirmation):                           │
│ To: customer@example.com                                   │
│ Subject: Booking Confirmation - [Reference]               │
│ Content: Booking details, reference, next steps            │
│                                                            │
│ Email 2 (Admin notification):                             │
│ To: admin@cleaningservices.com.au                         │
│ Subject: New Booking Request - [Reference]                │
│ Content: Full booking details, customer info              │
└─────────────┬───────────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Display success page                               │
├─────────────────────────────────────────────────────────────┤
│ • Show booking reference                                   │
│ • Confirm confirmation email sent                          │
│ • Show next steps                                          │
│ • Provide contact information                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Technology Stack Summary

```
BACKEND:
├─ Django 4.2.8
│  ├─ ORM (Object-Relational Mapping)
│  ├─ Built-in admin panel
│  ├─ Form handling & validation
│  ├─ Email system
│  └─ Authentication & authorization
│
├─ Python 3.8+
│
└─ SQLite (Development) / PostgreSQL (Production)

FRONTEND:
├─ HTML5
├─ CSS3
├─ Bootstrap 5.3
│  ├─ Responsive grid
│  ├─ Pre-built components
│  └─ Mobile-first design
│
├─ JavaScript (Vanilla)
│  ├─ Form validation
│  ├─ DOM manipulation
│  └─ User interactions
│
├─ Font Awesome (Icons)
│
├─ Google Fonts (Poppins, Inter)
└─ Custom CSS

SUPPORTING SERVICES:
├─ Email (SMTP)
├─ Image processing (Pillow)
├─ Form handling (Django Crispy Forms)
└─ Bootstrap components (Crispy Bootstrap 5)

DEPLOYMENT:
├─ Web Server: Gunicorn / uWSGI
├─ Reverse Proxy: Nginx
├─ Database: PostgreSQL
├─ Storage: S3 / CDN
├─ Email Service: SendGrid / AWS SES
└─ Hosting: Heroku / AWS / DigitalOcean
```

---

This architecture provides a solid, scalable foundation for a professional cleaning services website! 🏗️

