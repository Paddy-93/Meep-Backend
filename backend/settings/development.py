# backend/settings/development.py
"""
Development-specific Django settings overrides.

Extends the base settings with development-friendly configurations.
"""

from .base import *
import os

# Directory where static files will be collected during `collectstatic`
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable debug mode in development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']
