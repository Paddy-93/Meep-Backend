# users/serializers/register_serializer.py
import logging
from rest_framework import serializers
from users.models.custom_user import CustomUser
from users.email.email_verification import send_verification_email

logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user and triggering email verification.
    """

    # Make password write-only so it's never returned in API responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'role', 'company_name', 'password'
        ]

    def validate(self, data):
        """
        Validate incoming registration data before creating the user.
        Specifically ensures company_name is provided if user is a business.
        """
        logger.debug("🔍 Validating registration data: %s", data)
        if data.get('role') == CustomUser.Role.BUSINESS and not data.get('company_name'):
            logger.err("⚠️ Business user missing company name")
            raise serializers.ValidationError({
                "company_name": "This field is required for business users."
            })
        
        return data

    def create(self, validated_data):
        """
        Creates a new user after validation, and triggers an email verification
        if the user is not already verified.
        """
        logger.info("📦 Creating new user with: %s", validated_data)

        try:
            # Access request from serializer context, if available
            request = self.context.get('request')

            # Create user using custom create_user method to ensure password is hashed
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone_number=validated_data['phone_number'],
                role=validated_data.get('role', CustomUser.Role.PASSENGER),
                company_name=validated_data.get('company_name', ''),
                password=validated_data['password'],
            )

            logger.info("✅ User created: %s", user.email)

            # Send email verification if the user is not verified
            if request:
                logger.debug("✉️ Sending verification email to: %s", user.email)
                if not user.is_verified:
                    send_verification_email(user, request)

            return user

        except Exception as e:
            # Log and re-raise a user-friendly error on failure
            logger.error("❌ User creation failed", exc_info=True)
            raise serializers.ValidationError("User creation failed.")
