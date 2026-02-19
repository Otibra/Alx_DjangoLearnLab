from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .permissions import IsEditor, IsAdminUserCustom


class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    Supports filtering, searching, and ordering.
    Accessible by any user (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Anyone can view the list

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
    GET: Retrieve a single book by ID.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Only users in the 'Editors' group can create.
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
    PUT/PATCH: Update an existing book.
    Only users in the 'Editors' group can update.
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
    DELETE: Remove a book.
    Only users in the 'Admins' group can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserCustom]


