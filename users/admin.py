# users/admin.py

import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.custom_user import CustomUser

# Set up logger for the admin module
logger = logging.getLogger(__name__)

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the CustomUser model.
    Extends Django's built-in UserAdmin to manage additional fields.
    """

    model = CustomUser

    # Fields to display in the list view on the admin page
    list_display = (
        'email', 'first_name', 'last_name',
        'role', 'is_active', 'is_verified', 'is_staff'
    )

    # Filters available in the admin sidebar for easy filtering
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')

    # Fields available for searching
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

    # Default ordering of users in the list view (most recent first)
    ordering = ('-date_joined',)

    # Field groups and their fields in the detail view (user edit page)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_verified', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Role & Company', {'fields': ('role', 'company_name')}),
        ('Timestamps', {'fields': ('last_login', 'date_joined')}),
    )

    # Field groups and their fields in the "add user" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'phone_number',
                'password1', 'password2', 'role', 'is_verified'
            ),
        }),
    )


logger.info("✅ CustomUser registered successfully in Django Admin.")
