# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet that provides full CRUD operations for Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

