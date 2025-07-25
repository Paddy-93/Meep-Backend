"""
WSGI config for backend project.

This module exposes the WSGI callable as a module-level variable named `application`.
It serves as the entry point for WSGI-compatible web servers to serve your project.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' command.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")

# Get the WSGI application callable that the server uses to communicate with the Django app.
application = get_wsgi_application()