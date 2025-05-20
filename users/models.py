# Inheriting from Django’s built-in AbstractUser, which gives a 
# pre-made user model (with password hashing, login handling, etc.).
# The plan is to extend this base so it can be customized
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    Custom user model using email as the login identifier,
    with support for user roles and optional business fields.
    """
    email = models.EmailField(_('email address'), unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)

    class Role(models.TextChoices):
        PASSENGER = 'PASSENGER', _('Passenger')
        BUSINESS = 'BUSINESS', _('Business')
        DRIVER = 'DRIVER', _('Driver')

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PASSENGER,
        db_index=True,
    )

    company_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ['-created_at']