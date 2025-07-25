# users/email/email_verification_link.py
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

def generate_email_verification_link(user, request):
    """
    Generates a fully qualified email verification URL for the given user.

    The link includes a UID and token, and uses Django's default token generator
    to ensure the URL is unique and secure.

    Args:
        user (User): The user instance to verify.
        request (HttpRequest): The current HTTP request object to build the absolute URL.

    Returns:
        str: A fully qualified URL that can be sent via email for verification.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    relative_link = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
    return request.build_absolute_uri(relative_link)