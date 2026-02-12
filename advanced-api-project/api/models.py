from django.db import models

# Create your models here.

class Author(models.Model):
    # Stores the name of the author (max 200 characters)
    name = models.CharField(max_length=200)

    def __str__(self):
        # Returns the name of the author when printing the object
        # Useful in admin panel and debugging
        return self.name


class Book(models.Model):
    # Stores the title of the book (max 200 characters)
    title = models.CharField(max_length=200)
    
    # Stores the year the book was published as an integer
    publication_year = models.IntegerField()
    
    # ForeignKey relationship: each book has one author
    # on_delete=models.CASCADE -> if author is deleted, all their books are deleted
    # related_name='books' -> allows accessing all books of an author using author.books.all()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        # Returns the title of the book when printing the object
        return self.title
