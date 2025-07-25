#users/models/custom_user.py
import logging
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

#from common.logging_utils import log_with_context  # 👈 use centralized logging

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser.
    Handles creation of users and superusers using email instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            #log_with_context(logger, "error", "User creation failed: Email is required.", namespace="users.models.custom_user.create_user")
            logger.error("User creation failed: Email is required.")
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        #log_with_context(logger, "debug", f"Creating user with email: {email}", namespace="users.models.custom_user.create_user")
        logger.debug(f"Creating user with email: {email}")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        #log_with_context(logger, "info", f"User created successfully: {email}", namespace="users.models.custom_user.create_user")
        logger.info(f"User created successfully: {email}")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        #log_with_context(logger, "debug", f"Creating superuser: {email}", namespace="users.models.custom_user.create_superuser")
        logger.debug(f"Creating superuser: {email}")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            #log_with_context(logger, "error", "Superuser creation failed: is_staff must be True.", namespace="users.models.custom_user.create_superuser")
            logger.error("Superuser creation failed: is_staff must be True.")
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            #log_with_context(logger, "error", "Superuser creation failed: is_superuser must be True.", namespace="users.models.custom_user.create_superuser")
            logger.error("Superuser creation failed: is_superuser must be True.")
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the unique identifier.
    """

    class Role(models.TextChoices):
        PASSENGER = 'PASSENGER', _('Passenger')
        BUSINESS = 'BUSINESS', _('Business')

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

    phone_regex = RegexValidator(
        regex=r'^\+?[1-9]\d{7,14}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=15,
        unique=True,
        default="9999999999"
    )

    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.PASSENGER
    )

    company_name = models.CharField(
        _('company name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Only required if role is BUSINESS.')
    )

    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
