from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # ✅ Library imported here

# Function-based view: List all books
def list_all_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: Library details with its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
