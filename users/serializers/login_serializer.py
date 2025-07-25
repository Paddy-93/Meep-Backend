# users/serializers/login_serializer.py
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login using email and password.
    """
    email = serializers.EmailField() # User's email address
    password = serializers.CharField(write_only=True) # Password is write-only for security

    def validate(self, data):
        """
        Validates user credentials and ensures the user is active.
        Called automatically during serializer.is_valid().
        """
        user = authenticate(email=data['email'], password=data['password']) # Authenticate with custom backend

        if not user:
            raise serializers.ValidationError("Invalid login credentials") # Auth failed
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")  # User is disabled

        data['user'] = user  # Attach authenticated user to validated data
        return data
