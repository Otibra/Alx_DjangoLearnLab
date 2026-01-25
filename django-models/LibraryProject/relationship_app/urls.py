from django.urls import path
from .views import list_all_books, LibraryDetailView

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_all_books, name='list_all_books'),

    # Class-based view: library detail with its books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
