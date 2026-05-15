# relationship_app/query_samples.py

# Importing models from the current app's models.py file
from .models import Author, Book, Librarian, Library

# Django utility to return JSON responses
from django.http import JsonResponse


def list_books_in_library(library_name):
    # Fetch a Library object by its name (must exist or will raise DoesNotExist error)
    library = Library.objects.get(name=library_name)

    # Access all Book objects related to this library via the reverse relationship
    books = library.books.all()

    return books


def get_author_by_name(author_name):
    # Retrieve a single Author object matching the given name
    author = Author.objects.get(name=author_name)
    return author


def get_books_by_author(author):
    # Retrieve all Book objects written by the given author
    books = Book.objects.filter(author=author)
    return books


def get_librarian_by_library(library):
    # Retrieve the Librarian linked to a specific Library
    librarian = Librarian.objects.get(library=library)
    return librarian


def query_by_auth(request):
    # Get the 'author' parameter from the URL query string (e.g. ?author=John)
    author_name = request.GET.get('author')

    # If no author name is provided, return a 400 Bad Request response
    if not author_name:
        return JsonResponse({"error": "author parameter is required"}, status=400)

    # FIXED: correct field name should be 'author', not 'auther'
    # Filter books whose related author's name matches the given author_name
    books = Book.objects.filter(author__name=author_name)

    # Convert queryset into a list of dictionaries for JSON serialization
    data = list(books.values())

    # Return the filtered books as JSON response
    return JsonResponse({"books": data})


def get_books_in_library(library):
    # Return all books associated with the given Library instance
    return library.books.all()


def get_librarian(library):
    # Return the Librarian linked to the given Library instance
    return library.librarian
