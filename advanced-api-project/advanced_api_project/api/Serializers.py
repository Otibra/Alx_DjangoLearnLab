from rest_framework import serializers
from .models import Book
from .models import Author


# BookSerializer
# -----------------------------
# This serializer is responsible for converting Book model instances
# into JSON (or other content types) and validating incoming data
# when creating or updating Book objects via the API.
# Each Book is typically linked to an Author through a ForeignKey
# relationship defined in the Book model.
class BookSerializer(serializers.ModelSerializer):
     class Meta:
          #Specifies the model this serializer is based on
          model = Book
        # '__all__' means all fields from the Book model
        # will be included in the serialized output
          fields = '__all__'

# AuthorSerializer
# -----------------------------
# This serializer handles serialization and deserialization
# of Author model instances.
# Depending on how the Author model is defined, an Author can be
# related to multiple Book objects (one-to-many relationship).
class AuthorSerializer(serializers.ModelSerializer):
     
     class Meta:
          # Specifies the model this serializer is based on
          model = Author
          # Includes all fields defined on the Author model
          fields = '__all__'