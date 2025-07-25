# users/views/resend_verification_view.py

import logging

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.email.email_verification import send_verification_email

logger = logging.getLogger(__name__)
User = get_user_model()

class ResendVerificationThrottle(UserRateThrottle):
    rate = '3/min'

class ResendVerificationView(APIView):
    """
    Allows a user to request that the verification email be sent again.
    """

    throttle_classes = [ResendVerificationThrottle]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()

        if not email:
            logger.warning("⚠️ Email not provided in request")
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            validate_email(email)
        except ValidationError:
            logger.warning("🚫 Invalid email format: %s", email)
            return Response(
                {"detail": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning("❌ No user found with email: %s", email)
            return Response(
                {"detail": "No user found with this email address."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_verified:
            logger.info("🔒 User already verified: %s", email)
            return Response(
                {"detail": "This account is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            send_verification_email(user, request)
            logger.info("📨 Verification email resent to: %s", email)
            return Response(
                {"detail": "Verification email has been resent."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception("❌ Failed to send verification email to %s", email)
            return Response(
                {"detail": "Failed to send verification email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
