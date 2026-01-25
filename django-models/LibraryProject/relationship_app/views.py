from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-Based View: List all books with their authors
def list_all_books(request):
    books = Book.objects.all()
    output = ""

    for book in books:
        output += f"{book.title} by {book.author.name}\n"

    return HttpResponse(output, content_type="text/plain")


# Class-Based View: Display details of a specific library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context

