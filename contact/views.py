from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .forms import ContactForm


class ContactPageView(TemplateView):
    template_name = 'contact/contact.html'


def contact_message_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            # Send confirmation email to customer
            try:
                subject = f'Thank you for contacting {settings.BUSINESS_NAME}'
                body = f"""
Hello {message.full_name},

Thank you for reaching out to {settings.BUSINESS_NAME}. 
We have received your message and will get back to you as soon as possible.

Your Message:
{message.message}

Best regards,
{settings.BUSINESS_NAME}
Contact: {settings.BUSINESS_PHONE}
"""
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [message.email])
            except Exception as e:
                print(f"Error sending confirmation email: {e}")

            # Send notification to admin
            try:
                admin_subject = f'New Contact Message from {message.full_name}'
                admin_body = f"""
New contact message received:

Name: {message.full_name}
Email: {message.email}
Phone: {message.phone}
Subject: {message.subject}

Message:
{message.message}
"""
                send_mail(admin_subject, admin_body, settings.DEFAULT_FROM_EMAIL, [settings.BUSINESS_EMAIL])
            except Exception as e:
                print(f"Error sending admin notification: {e}")

            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact:contact-success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact-form.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/contact-success.html')
