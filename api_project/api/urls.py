from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList
from .views import BookViewSet

# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')  # <-- changed here

urlpatterns = [
    # Optional: keep BookList if you want a read-only list (can remove if not needed)
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
]
