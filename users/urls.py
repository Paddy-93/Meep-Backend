# users/urls.py
"""
URL configuration for user-related endpoints.

This file defines the routing for authentication and user management views such as:
- User registration
- Login
- Email verification
- Resending verification emails

Each endpoint is mapped to a corresponding class-based view located in `users.views`.

Endpoints:
- POST /register/                  -> Register a new user
- POST /login/                     -> Authenticate user and return token
- GET  /verify-email/<uidb64>/<token>/ -> Verify user's email address
- POST /resend-verification-email/ -> Resend verification email for unverified users

These URLs are typically included in the project's root `urls.py` as a namespace or part of a larger API routing setup.
"""
from django.urls import path
from users.views.register_view import RegisterView
from users.views.login_view import LoginView
from users.views.verify_email_view import VerifyEmailView
from users.views.resend_verification_view import ResendVerificationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-email/', ResendVerificationView.as_view(), name='resend-verification-email')
]
