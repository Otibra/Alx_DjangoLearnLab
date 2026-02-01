# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books.
    """
    queryset = Book.objects.all()        # Query all Book objects
    serializer_class = BookSerializer    # Use BookSerializer for output
