from django.urls import path
from .views import list_books  # ✅ must match this exact name
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_books, name='list_books'),

    # Class-based view: library detail with its books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
