# relationship_app/query_samples.py

import django
import os

# Setup Django environment (adjust path if needed)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.book_set.all()  # Default reverse name without related_name
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with the name '{author_name}'")

# 2️⃣ List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # ManyToManyField still uses .all()
        print(f"Books in {library_name} Library:")
        for book in books:
            print(f"- {book.title} (Author: {book.author.name})")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'")

# 3️⃣ Retrieve the librarian for a library
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # OneToOneField reverse still works
        print(f"Librarian of {library_name} Library: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}' Library")

