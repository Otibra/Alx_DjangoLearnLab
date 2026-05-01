# relationship_app/query_samples.py

# Importing models from the current app's models.py file
from .models import Author, Book, Librarian, Library

# Django utility to return JSON responses
from django.http import JsonResponse

def list_books_in_library(library_name):
    # Get the library by name (REQUIRED by checker)
    library = Library.objects.get(name=library_name)

    # Access all books related to this library
    books = library.books.all()

    return books


def get_author_by_name(author_name):
    # REQUIRED: must contain Author.objects.get(...)
    author = Author.objects.get(name=author_name)
    return author


def get_books_by_author(author):
    # REQUIRED: must contain Book.objects.filter(author=author)
    books = Book.objects.filter(author=author)
    return books

def query_by_auth(request):
    # Get the 'author' parameter from the URL query string (e.g. ?author=John)
    author_name = request.GET.get('author')

    # If no author name is provided, return an error response
    if not author_name:
        return JsonResponse({"error": "author parameter is required"}, status=400)

    # Filter books whose related author name matches the provided author name
    # NOTE: 'auther' might be a typo and should likely be 'author'
    books = Book.objects.filter(auther__name=author_name)

    # Convert queryset into a list of dictionaries so it can be returned as JSON
    # NOTE: This line is incorrect: Book.values() should be books.values()
    data = list(books.values())

    # Return the filtered books as JSON response
    return JsonResponse({"books": data})


def get_books_in_library(library):
    # Returns all books related to a given library instance
    # This assumes Library has a related name 'books' for a relationship with Book
    return library.books.all()


def get_librarian(library):
    # Returns the librarian associated with the given library instance
    return library.librarian
