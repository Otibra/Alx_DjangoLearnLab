import django_filters
from .models import Book

# Define a custom FilterSet for advanced filtering
class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for Book model.
    Enables exact matches, range filtering, and partial title matching.
    """
    author = django_filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    publication_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='exact')
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['author', 'publication_year', 'title']
