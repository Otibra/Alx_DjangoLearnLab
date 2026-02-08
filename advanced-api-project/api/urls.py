from django.urls import path
from .views import BookListView
from .views import BookDetailView
from .views import BookCreateView
from .views import BookUpdateView
from .views import BookDeleteView

urlpatterns = [
    # List all books
    path("", BookListView.as_view(), name="book-list"),  # /books/

    # Show details of a single book
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),  # /books/<int:pk>/

    # Create a new book
    path("create/", BookCreateView.as_view(), name="book-create"),  # /books/create/

    # Update an existing book
    path("<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),  # /books/<int:pk>/update/

    # Delete a book
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),  # /books/<int:pk>/delete/
]
