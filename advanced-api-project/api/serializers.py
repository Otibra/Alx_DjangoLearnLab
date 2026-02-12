# Import models from the current app
from .models import Book
from .models import Author
# Import date class to get the current year
from datetime import date
# Import Django REST Framework serializers
from rest_framework import serializers

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # Connect this serializer to the Book model
        model = Book
        # Include all fields of the Book model
        fields = '__all__'

    # Field-level validation for the publication_year field
    def validate_publication_year(self, value):
        # Get the current year
        current_year = date.today().year
        # Check if the provided year is in the future
        if value > current_year:
            # Raise an error if publication year is invalid
            raise serializers.ValidationError("Publication year cannot be in the future.") 
        # Return the valid year
        return value


# Serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to show all books of an author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        # Connect this serializer to the Author model
        model = Author
        # Include all fields of the Author model
        fields = '__all__'
