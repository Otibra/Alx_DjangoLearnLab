from django.contrib import admin
from .models import Library
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
from .models import UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Library)

# users/admin.py
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # Fields displayed in admin list page
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_of_birth',
        'is_staff',
    )

    # Add custom fields to the user detail page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            )
        }),
    )

    # Add custom fields when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            )
        }),
    )
  