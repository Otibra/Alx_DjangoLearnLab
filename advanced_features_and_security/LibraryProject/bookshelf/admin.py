
from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register the Book model with custom admin options
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters by author and publication year
    list_filter = ('author', 'publication_year')
    
    # Enable search by title and author
    search_fields = ('title', 'author')

# admin.py
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    # Fields displayed in the admin user list
    list_display = (
        'username',
        'email',
        'date_of_birth',
        'is_staff',
        'is_superuser',
    )

    # Add custom fields to the admin detail page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            ),
        }),
    )

    # Add custom fields when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
 