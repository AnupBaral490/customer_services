"""
Django settings for Cleaning Services project.
Production-ready configuration for Australian cleaning company website.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Note: BASE_DIR is the project root (parent of config/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8ez)m_vgo5slot6v&m^==n61vf-g2no=fbw@)dt!yxh64&fqig')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    # Local apps
    'core.apps.CoreConfig',
    'services.apps.ServicesConfig',
    'bookings.apps.BookingsConfig',
    'customers.apps.CustomersConfig',
    'contact.apps.ContactConfig',
    'dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.business_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'config' / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization - Australian settings

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_TZ = True

DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'd/m/Y H:i'

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication settings
LOGIN_URL = 'customers:customer-login'
LOGIN_REDIRECT_URL = '/'

# Crispy Forms configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email configuration
# Now using SMTP backend for actual email delivery to Gmail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'baralanup832@gmail.com'
EMAIL_HOST_PASSWORD = 'lszg npgx cdfx vbmu'  # Gmail app password
DEFAULT_FROM_EMAIL = 'baralanup832@gmail.com'

# IMPORTANT: If emails are not being delivered:
# 1. Check https://myaccount.google.com/security for "Less secure app access"
# 2. Or create a separate Gmail account specifically for this app
# 3. See GMAIL_DELIVERY_FIX.md for complete troubleshooting guide
# 
# The email is being SENT successfully (verified by diagnostic tool),
# but Gmail may be blocking delivery due to security settings.

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Business information - can be overridden via environment variables
BUSINESS_NAME = os.environ.get('BUSINESS_NAME', 'Raslan Cleaning Services')
BUSINESS_PHONE = os.environ.get('BUSINESS_PHONE', '+61 2 1234 5678')
BUSINESS_EMAIL = os.environ.get('BUSINESS_EMAIL', 'hello@cleaningservices.com.au')
BUSINESS_ADDRESS = os.environ.get('BUSINESS_ADDRESS', 'Sydney, NSW 2000, Australia')
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '61412345678')
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
