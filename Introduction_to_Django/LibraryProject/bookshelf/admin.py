
from django.contrib import admin
from .models import Book

# Register the Book model with custom admin options
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters by author and publication year
    list_filter = ('author', 'publication_year')
    
    # Enable search by title and author
    search_fields = ('title', 'author')
