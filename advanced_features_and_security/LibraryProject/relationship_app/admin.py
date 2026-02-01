# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .models import Author
from .models import Book
from .models import Library
from .models import Librarian


# ----------------------
# Custom User Admin
# ----------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Includes custom fields: date_of_birth and profile_photo.
    """

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Author Admin
# ----------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


# ----------------------
# Book Admin
# ----------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("title",)


# ----------------------
# Library Admin
# ----------------------
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("books",)


# ----------------------
# Librarian Admin
# ----------------------
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("user", "library")
