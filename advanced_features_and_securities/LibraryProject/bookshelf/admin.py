from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Book

# ----------------------
# Custom User Admin
# ----------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Book Admin
# ----------------------
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year", "owner")
    list_filter = ("publication_year",)
    search_fields = ("title", "author", "owner__username")


# ----------------------
# Register models
# ----------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
