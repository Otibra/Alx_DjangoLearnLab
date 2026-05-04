from django.shortcuts import render,redirect 
from django.views.generic.detail import DetailView
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

from .models import Book
from .models import Library


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

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


#.......home view...............
#........... login_required......

@login_required
def home_view(request):
    return render(request, 'home.html')

