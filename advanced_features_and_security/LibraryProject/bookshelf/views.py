from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

from .models import Book
from .forms import ExampleForm


# -----------------------------
# View Books
# -----------------------------
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):

    books = Book.objects.all()

    response = render(request, 'bookshelf/book_list.html', {
        'books': books
    })

    # Security Header
    response["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self';"
    )

    return response


# -----------------------------
# Create Book
# -----------------------------
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):

    if request.method == 'POST':

        # Validate and sanitize input
        form = ExampleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('book_list')

    else:
        form = ExampleForm()

    return render(request, 'bookshelf/create_book.html', {
        'form': form
    })


# -----------------------------
# Edit Book
# -----------------------------
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        # Validate edited data
        form = ExampleForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('book_list')

    else:
        form = ExampleForm(instance=book)

    return render(request, 'bookshelf/edit_book.html', {
        'form': form
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

    return render(request, 'bookshelf/delete_book.html', {
        'book': book
    })


# -----------------------------
# Add Book
# -----------------------------
def add_book(request):

    if request.method == "POST":

        form = ExampleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("book_list")

    else:
        form = ExampleForm()

    return render(request, "bookshelf/add_book.html", {
        "form": form
    })
