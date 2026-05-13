from django.shortcuts import render, redirect, get_object_or_404 
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from .models import CustomUser


from .models import Book
from .models import Library
from .forms import BookForm


# Book & Library Views
# ----------------------

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# A class-based view to display details of a single Library object
class LibraryDetailView(DetailView):
    # Specifies the model to retrieve data from
    model = Library
    
    # Template used to render the library detail page
    template_name = 'relationship_app/library_detail.html'
    
    # The name used to refer to the object in the template context
    context_object_name = 'library'

    # Override the default method to add extra context data
    def get_context_data(self, **kwargs):
        # Get the default context data (includes the library object)
        context = super().get_context_data(**kwargs)
        
        # Add all books related to this library into the context
        # Assumes a related_name='books' on a ForeignKey or ManyToManyField
        context['books'] = self.object.books.all()
        
        # Return the updated context dictionary
        return context
    
    #............register user........

def register(request):
    if request.method == "POST":
        form =UserCreationForm (request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form =UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


#.......home view...............
#........... login_required......

@login_required
def home_view(request):
    return render(request, 'relationship_app/home.html')


# Role test functions
def is_admin(user):
    return user.userprofile.role == 'ADMIN'


def is_librarian(user):
    return user.userprofile.role == 'Librarian'


def is_member(user):
    return user.userprofile.role == 'Member'


# Admin View
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# Librarian View
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


# Member View
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

#......add book....
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):

    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_book')

    else:
        form = BookForm()

    return render(request, 'relationship_app/add_book.html', {'form': form})

#.......edit book....
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('list_book')

    else:
        form = BookForm(instance=book)

    return render(request, 'relationship_app/edit_book.html', {'form': form})

#......delete book......
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect('list_book')

    return render(request, 'relationship_app/delete_book.html', {'book': book})




