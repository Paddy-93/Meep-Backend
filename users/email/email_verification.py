# users/email/email_verification.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from users.email.email_verification_link import generate_email_verification_link

import logging
logger = logging.getLogger(__name__)

def send_verification_email(user, request):
    """
    Sends a verification email to the user with a unique token link.

    Args:
        user (User): The user to send the email to.
        request (HttpRequest): The current request object, used to build absolute URLs.
    """
    verification_url = generate_email_verification_link(user, request)

    subject = 'Verify Your Email Address'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    context = {
        'user': user,
        'verification_url': verification_url,
    }

    html_content = render_to_string('users/verify_email.html', context)

    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send(fail_silently=False)
    except Exception as e:
        logger.error("Email sending failed", exc_info=True)