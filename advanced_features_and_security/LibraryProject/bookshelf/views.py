from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
# Create your views here.

# -----------------------------
# View Books
# -----------------------------
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):

    books = Book.objects.all()

    return render(request, 'books/book_list.html', {
        'books': books
    })


# -----------------------------
# Create Book
# -----------------------------
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')

        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year
        )

        return redirect('book_list')

    return render(request, 'books/create_book.html')


# -----------------------------
# Edit Book
# -----------------------------
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')

        book.save()

        return redirect('book_list')

    return render(request, 'books/edit_book.html', {
        'book': book
    })


# -----------------------------
# Delete Book
# -----------------------------
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'books/delete_book.html', {
        'book': book
    })
