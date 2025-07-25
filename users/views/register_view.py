# users/views/register_view.py
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers.register_serializer import RegisterSerializer
from users.serializers.user_serializer import UserSerializer

from users.email.email_verification import send_verification_email

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    """
    Handles user registration and sends a verification email.
    """

    def post(self, request):
        logger.info("📩 Registration data received: %s", request.data)
        serializer = RegisterSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info("✅ User created: %s", user.email)

                return Response({
                    "message": "Registration successful. Please check your email to verify your account.",
                    "user": UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.exception("❌ Error during registration")
                return Response({
                    "message": "Internal server error during registration."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning("⚠️ Registration failed validation: %s", serializer.errors)
        return Response({
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

