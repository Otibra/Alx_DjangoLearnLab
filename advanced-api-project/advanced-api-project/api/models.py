from django.db import models

# Create your models here.
# The Author model represents a writer who can have one or more books.
# Each Author instance corresponds to a single author in the database.
class Author(models.Model):
    # Stores the full name of the author.
    # max_length=200 limits the number of characters allowed in the database.
    name = models.CharField(max_length = 200)
    # This method defines how the Author object is displayed as a string.
    # It is used in the Django admin panel and shell for readability.
    def __str__(self):
        return self.name
# The Book model represents a book written by an author.
# Each Book instance is linked to exactly one Author.
class Book(models.Model):
    # Stores the title of the book.
    title = models.CharField(max_length = 200)
    # Stores the year the book was published.
    # IntegerField is appropriate since only a year (number) is needed
    publication_year = models.IntegerField()
    # Creates a many-to-one relationship between Book and Author.
    # - Each book has one author.
    # - on_delete=models.CASCADE means if an author is deleted,
    #   all their books will also be deleted.
    # - related_name="books" allows access like author.books.all()
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "books")
    # Defines the string representation of the Book object.
    # This helps display the book title in the admin interface.
    def __str__(self):
        return self.title