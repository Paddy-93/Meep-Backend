#!/usr/bin/env python
"""
manage.py — Django’s command-line utility for administrative tasks,
enhanced with startup logging for better visibility in development and production.

Usage:
    python manage.py <command>
Example:
    python manage.py runserver
"""

import os
import sys
import logging
from datetime import datetime

def setup_startup_logger():
    """
    Configure startup logging before Django settings are loaded.

    Returns:
        logging.Logger: Configured logger for startup tasks.
    """
    log_file = os.path.join(os.path.dirname(__file__), 'startup.log')
    logger = logging.getLogger('startup')
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():  # Avoid duplicate handlers on reload
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

logger = setup_startup_logger()

def main():
    """
    Main entry point for Django's management commands.
    Initializes settings and delegates to Django’s CLI utility.
    """
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')
        logger.debug("🛠 Using settings module: backend.settings.development")

        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.critical(
            "❌ Django import failed. Ensure your virtual environment is activated and dependencies installed.",
            exc_info=True
        )
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and your virtual environment is active."
        ) from exc

    logger.info(f"📦 Running Django command: {' '.join(sys.argv)}")
    try:
        execute_from_command_line(sys.argv)
        logger.info("✅ Command execution completed successfully.")
    except Exception:
        logger.error("❌ Error while executing Django command.", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("🚀 Django management script started at %s", datetime.now())
    main()
