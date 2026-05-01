from django.urls import path
from .views import LibraryDetailView,list_books

urlpatterns =[
    path('books/', list_books, name='list_books'),

    # Class-based view: shows details of a single library
    # The <int:pk> is required because DetailView expects a primary key by default
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]