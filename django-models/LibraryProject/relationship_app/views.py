from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

from .models import Book
from .models import Library


# ----------------------
# Book & Library Views
# ----------------------

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ----------------------
# Permission-Based Book CRUD
# ----------------------

@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        Book.objects.create(title=title, author_id=author_id)
        return redirect("list_books")
    return render(request, "relationship_app/add_book.html")


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.save()
        return redirect("list_books")
    return render(request, "relationship_app/edit_book.html", {"book": book})


@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})


# ----------------------
# Authentication Views
# ----------------------

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


# ----------------------
# Role Check Functions
# ----------------------

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == "Admin"


def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == "Librarian"


def is_member(user):
    return user.is_authenticated and user.userprofile.role == "Member"


# ----------------------
# Role-Based Views
# ----------------------

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
