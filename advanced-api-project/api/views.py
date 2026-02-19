# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, permissions, status
from .permissions import IsEditor, IsAdminUserCustom


class BookListView(generics.ListAPIView):
    """
    A ListView for retrieving all books.
    Supports filtering, searching, and ordering.
    Accessible by any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['author', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['publication_year', 'title']


class BookDetailView(generics.RetrieveAPIView):
    """
    A DetailView for retrieving a single book by ID.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookCreateView(generics.CreateAPIView):
    """
    A CreateView for adding a new book.
    Only users with editor role can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEditor]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "Book created successfully",
                "data": response.data
            },
            status=status.HTTP_201_CREATED
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    An UpdateView for modifying an existing book.
    Only users with editor role can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEditor]

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Book updated successfully",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    A DeleteView for removing a book.
    Only admin users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserCustom]


# ================================
# Key Notes:
# - A ListView for retrieving all books.
# - A DetailView for retrieving a single book by ID.
# - A CreateView for adding a new book.
# - An UpdateView for modifying an existing book.
# - A DeleteView for removing a book.
# ================================
