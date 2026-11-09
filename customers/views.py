from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
import logging
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerProfileForm
from .models import CustomerProfile

logger = logging.getLogger(__name__)


def send_welcome_email(user):
    """Send welcome email to new customer on signup."""
    try:
        subject = f'Welcome to {settings.BUSINESS_NAME}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 28px;">Welcome, {user.first_name}!</h1>
                        <p style="color: #666; margin: 0; font-size: 16px;">We're excited to have you join our community</p>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #DCA85C;">
                        <p style="margin-bottom: 15px;">Thank you for creating an account with <strong>{settings.BUSINESS_NAME}</strong>.</p>
                        
                        <p style="margin-bottom: 15px;">Your account is now active, and you can:</p>
                        <ul style="margin: 15px 0; padding-left: 20px;">
                            <li>Book our professional cleaning services</li>
                            <li>Request custom quotes</li>
                            <li>Manage your profile and preferences</li>
                            <li>Track your bookings and history</li>
                        </ul>

                        <p style="margin-bottom: 20px;">Your account details:</p>
                        <div style="background: #DCEFE8; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                            <p style="margin: 5px 0;"><strong>Name:</strong> {user.get_full_name()}</p>
                            <p style="margin: 5px 0;"><strong>Email:</strong> {user.email}</p>
                        </div>

                        <p style="margin-bottom: 20px;">If you have any questions or need assistance, our team is here to help!</p>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="{settings.SITE_URL}/customers/profile/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            Go to Your Profile
                        </a>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 14px;">
                        <p style="margin: 5px 0;">
                            <strong>{settings.BUSINESS_NAME}</strong><br>
                            Phone: {settings.BUSINESS_PHONE}<br>
                            Email: {settings.BUSINESS_EMAIL}
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        send_mail(
            subject,
            f'Welcome to {settings.BUSINESS_NAME}. Your account is ready to use.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending welcome email to {user.email}: {e}")
        print(f"Error sending welcome email: {e}")
        return False


def send_first_login_email(user):
    """Send first login notification email."""
    try:
        subject = f'First Login Confirmed - {settings.BUSINESS_NAME}'
        html_message = f"""
        <html>
            <body style="font-family: 'Inter', Arial, sans-serif; color: #252B2A; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background: #F7F9F8; padding: 40px 20px; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #183D39; margin: 0 0 10px 0; font-size: 24px;">Account Activated!</h1>
                        <p style="color: #666; margin: 0; font-size: 16px;">Your first login has been confirmed</p>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 8px; border-left: 4px solid #10B981;">
                        <p style="margin-bottom: 20px;">Hi {user.first_name},</p>
                        
                        <p style="margin-bottom: 20px;">Great! You've successfully logged into your {settings.BUSINESS_NAME} account for the first time. Your account is now fully activated and ready to use.</p>

                        <div style="background: #DCEFE8; padding: 20px; border-radius: 6px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #183D39;">What you can do now:</h3>
                            <ul style="margin: 10px 0; padding-left: 20px;">
                                <li><strong>Book Services:</strong> Schedule cleaning appointments at your convenience</li>
                                <li><strong>Request Quotes:</strong> Get personalized pricing for your needs</li>
                                <li><strong>Manage Profile:</strong> Update your information and preferences</li>
                                <li><strong>Track Bookings:</strong> View your booking history and status</li>
                            </ul>
                        </div>

                        <p style="margin-bottom: 15px;">If you need any assistance or have questions, our team is available to help:</p>
                        <p style="margin: 0;">
                            <strong>Phone:</strong> {settings.BUSINESS_PHONE}<br>
                            <strong>Email:</strong> {settings.BUSINESS_EMAIL}
                        </p>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="{settings.SITE_URL}/bookings/booking/" 
                           style="display: inline-block; background: #183D39; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-right: 10px;">
                            Book Now
                        </a>
                        <a href="{settings.SITE_URL}/bookings/quote/" 
                           style="display: inline-block; background: #DCA85C; color: #183D39; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">
                            Request Quote
                        </a>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E8E8E8; text-align: center; color: #666; font-size: 12px;">
                        <p style="margin: 0;">This is an automated email. Please do not reply directly to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        send_mail(
            subject,
            f'Your first login to {settings.BUSINESS_NAME} has been confirmed.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=True,
        )
        logger.info(f"First login email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending first login email to {user.email}: {e}")
        print(f"Error sending first login email: {e}")
        return False


@require_http_methods(["GET", "POST"])
def customer_signup(request):
    """Customer registration view."""
    if request.user.is_authenticated:
        return redirect('customers:customer-profile')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user)
            login(request, user)
            messages.success(request, 'Registration successful! Check your email for a welcome message.')
            return redirect('customers:customer-profile')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customers/signup.html', {'form': form, 'page_title': 'Create Account'})


@require_http_methods(["GET", "POST"])
def customer_login(request):
    """Customer login view."""
    if request.user.is_authenticated:
        return redirect('customers:customer-profile')
    
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    # Get or create profile to check if this is first login
                    profile, created = CustomerProfile.objects.get_or_create(user=user)
                    
                    # Send first login email only on first login
                    if created or not profile.last_login_notified:
                        send_first_login_email(user)
                        profile.last_login_notified = True
                        profile.save()
                    
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    next_url = request.GET.get('next', 'customers:customer-profile')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid email or password.')
            except:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'customers/login.html', {'form': form, 'page_title': 'Customer Login'})


@login_required(login_url='customers:customer-login')
@require_http_methods(["GET", "POST"])
def customer_profile(request):
    """Customer profile view."""
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('customers:customer-profile')
    else:
        form = CustomerProfileForm(instance=profile, user=request.user)
    
    # Get customer's bookings and quotes
    from bookings.models import Booking, QuoteRequest
    bookings = Booking.objects.filter(customer__email=request.user.email).order_by('-created_at')
    quotes = QuoteRequest.objects.filter(customer__email=request.user.email).order_by('-created_at')
    
    context = {
        'form': form,
        'page_title': 'My Profile',
        'bookings': bookings[:5],
        'quotes': quotes[:5],
    }
    return render(request, 'customers/profile.html', context)


@login_required(login_url='customers:customer-login')
@require_http_methods(["POST"])
def customer_logout(request):
    """Customer logout view - handles both GET and POST."""
    if request.method in ['GET', 'POST']:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('core:home')
    return redirect('core:home')
