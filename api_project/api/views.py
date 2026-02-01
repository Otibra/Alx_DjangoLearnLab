# Create your views here.
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books (read-only).
    Only accessible to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # require login to view


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet that provides full CRUD operations for Book.
    Authenticated users can read; only admin users can create/update/delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]

    # Default permission
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Apply custom permissions per action:
        - Safe methods (GET, HEAD, OPTIONS) → any authenticated user
        - Create/Update/Delete → admin only
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]  # only admins can modify
        else:
            permission_classes = [IsAuthenticated]  # authenticated users can read
        return [permission() for permission in permission_classes]

