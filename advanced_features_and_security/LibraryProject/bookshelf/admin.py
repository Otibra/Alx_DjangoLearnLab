from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Book

# ----------------------
# Custom User Admin
# ----------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to display in admin list view
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )

    # Fields to filter by in admin list view
    list_filter = ("is_staff", "is_active")

    # Fields available in the user detail form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields for creating a new user in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Register models
# ----------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)

    

