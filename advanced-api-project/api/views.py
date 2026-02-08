from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from .models import Book


# ------------------------------
# PUBLIC PAGES — anyone can see
# ------------------------------

class BookListView(ListView):
    """Show a list of all books. Open to everyone."""
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"


class BookDetailView(DetailView):
    """Show details for a single book. Open to everyone."""
    model = Book
    template_name = "books/book_detail.html"


# ------------------------------
# RESTRICTED PAGES — login required
# ------------------------------

class BookCreateView(LoginRequiredMixin, CreateView):
    """Allow logged-in users to create a new book."""
    model = Book
    fields = ["title", "publication_year", "author"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("book-list")
    login_url = "/accounts/login/"

    def form_valid(self, form):
        # Prevent future pub_year  and  pub_year = form.cleaned_data.get("publication_year")
        if pub_year and pub_year > date.today().year:
            form.add_error("publication_year", "Publication year cannot be in the future.")
            return self.form_invalid(form)

        messages.success(self.request, f"Book '{form.instance.title}' was created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Oops! There was an error creating the book. Please check the form.")
        return super().form_invalid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """Allow logged-in users to update an existing book."""
    model = Book
    fields = ["title", "publication_year", "author"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("book-list")
    login_url = "/accounts/login/"

    def form_valid(self, form):
        pub_year = form.cleaned_data.get("publication_year")
        if pub_year and pub_year > date.today().year:
            form.add_error("publication_year", "Publication year cannot be in the future.")
            return self.form_invalid(form)

        messages.success(self.request, f"Book '{form.instance.title}' was updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Oops! There was an error updating the book. Please check the form.")
        return super().form_invalid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """Allow logged-in users to delete a book."""
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("book-list")
    login_url = "/accounts/login/"

