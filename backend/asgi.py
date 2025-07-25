# backend/asgi.py

"""
ASGI config for the backend project.

This file exposes the ASGI callable as a module-level variable named ``application``.

ASGI (Asynchronous Server Gateway Interface) is the standard for asynchronous Python web apps and servers.

More on ASGI: https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for ASGI.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")

# Expose the ASGI application.
application = get_asgi_application()
