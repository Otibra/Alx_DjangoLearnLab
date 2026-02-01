# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Import CustomUser from the app where it is defined (bookshelf)
from bookshelf.models import CustomUser
from .models import Book  # Your Book model in this app


# ----------------------
# Custom User Admin
# ----------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser.
    Adds date_of_birth and profile_photo fields.
    """

    # Show these fields when viewing/editing a user
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    # Show these fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    # Columns to display in user list
    list_display = ("username", "email", "is_staff", "is_active", "date_of_birth")
    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Book Admin
# ----------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")

