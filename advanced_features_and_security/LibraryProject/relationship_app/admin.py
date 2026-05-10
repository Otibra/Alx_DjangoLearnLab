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

 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # Fields displayed in admin list view
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )

    # Fields used for searching
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    # Filters in right sidebar
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # Add custom fields to existing UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "date_of_birth",
                    "profile_photo",
                )
            },
        ),
    )

    # Fields shown when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "classes": ("wide",),
                "fields": (
                    "date_of_birth",
                    "profile_photo",
                ),
            },
        ),
    )
    