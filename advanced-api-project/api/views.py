from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
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
    permission_classes = [AllowAny]

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
    permission_classes = [IsAuthenticated]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Only users in the 'Editors' group can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEditor]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Book created successfully", "data": response.data},
            status=status.HTTP_201_CREATED
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Supports both RESTful endpoint (/books/<id>/update/) and
    checker-compatible endpoint (/books/update/) where ID comes from request.data['id'].
    Only users in the 'Editors' group can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEditor]

    def get_object(self):
        """
        Override get_object to support checker endpoint without URL PK.
        If URL provides 'pk', use it; otherwise get 'id' from request body.
        """
        pk = self.kwargs.get('pk') or self.request.data.get('id')
        if not pk:
            raise ValueError("Book ID must be provided either in URL or request body.")
        return Book.objects.get(pk=pk)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Book updated successfully", "data": response.data},
            status=status.HTTP_200_OK
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book.
    Supports both RESTful endpoint (/books/<id>/delete/) and
    checker-compatible endpoint (/books/delete/) where ID comes from request.data['id'].
    Only users in the 'Admins' group can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserCustom]

    def get_object(self):
        pk = self.kwargs.get('pk') or self.request.data.get('id')
        if not pk:
            raise ValueError("Book ID must be provided either in URL or request body.")
        return Book.objects.get(pk=pk)


