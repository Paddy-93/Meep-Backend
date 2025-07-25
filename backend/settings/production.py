# backend/settings/production.py
"""
Production-specific Django settings overrides.

Extends the base settings with production-ready configurations.
"""

from .base import *
from decouple import config, Csv

# Disable debug mode in production
DEBUG = False

# Set allowed hosts from environment variables, cast as a list
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv)

# TODO: Add production database configuration, security settings, and other production-specific overrides here.
