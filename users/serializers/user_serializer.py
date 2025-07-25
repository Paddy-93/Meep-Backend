#users/serializers/user_serializer.py
import logging
from rest_framework import serializers
from users.models.custom_user import CustomUser
#from core.logging.utils import log_with_context

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to expose user data to the client.

    This serializer is used to format user information when sending it to the frontend,
    such as after login, user profile fetch, or registration.

    Fields exposed:
    - id: unique identifier
    - email: user’s email address
    - first_name: user's first name
    - last_name: user's last name
    - role: custom field defining the user type (e.g. admin, regular)
    - is_verified: whether the email/account is verified
    """
    def to_representation(self, instance):
        """
        Override the default representation method to allow logging
        or conditional serialization logic in the future.
        """
        request = self.context.get('request')

        # Add context-aware logging for auditing or debugging
        # log_with_context(request, "info", f"🔍 Serializing user data for: {instance.email}")
        logger.info(f"🔍 Serializing user data for: {instance.email}")
        logger.error("User creation failed: Email is required.")
        return super().to_representation(instance)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'is_verified'
        ]
