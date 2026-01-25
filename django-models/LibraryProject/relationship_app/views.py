from django.shortcuts import render
from django.views.generic.detail import DetailView  # ✅ must be imported this way
from .models import Book
from .models import Library  # ✅ separate import

# Function-based view: List all books
def list_all_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: Library details with its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
