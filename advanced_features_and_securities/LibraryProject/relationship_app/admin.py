from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bookshelf.models import CustomUser  # Import your custom user
from .models import Book                  # Your Book model in this app


# ----------------------
# Custom User Admin
# ----------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin for CustomUser with additional fields: date_of_birth, profile_photo.
    """

    # Add extra fields to the existing UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    # Add extra fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    # Columns to display in user list view
    list_display = ("username", "email", "is_staff", "is_active", "date_of_birth")
    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Book Admin
# ----------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year", "owner")  # Show owner
    search_fields = ("title", "author", "owner__username")
    list_filter = ("publication_year",)

