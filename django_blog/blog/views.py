from django.shortcuts import render, redirect
from django.contrib import messages  # Used for showing success or info messages
from django.contrib.auth.decorators import login_required  # Protects views from anonymous users
from .forms import UserUpdateForm, PostForm
from .models import Post
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def profile(request):
    """
    Allows an authenticated user to view and edit their profile.
    
    Step-by-step:
    1. @login_required ensures only logged-in users can access this view.
    2. Check if the request method is POST:
        - This means the user submitted the form to update their info.
        - Bind the form with POST data and the current user instance.
        - Validate the form:
            - If valid, save the updated data to the database.
            - Show a success message using Django's messages framework.
            - Redirect back to the same profile page to avoid resubmission.
    3. If the request method is GET:
        - Display the form pre-filled with the current user's data.
    4. Render 'profile.html' and pass the form to the template.
    """
    if request.method == 'POST':
        # Bind form with submitted data
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():  # Check for validation errors
            form.save()  # Save updated username/email
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to refresh the page
    else:
        # Display the form with current user data
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

class PostListView(ListView):
    """
    View to display all blog posts in reverse chronological order.
    Supports pagination to show a limited number of posts per page.
    """
    model = Post
    template_name = 'blog/post_list.html'  # Template to render
    context_object_name = 'posts'          # Context variable in template
    ordering = ['-published_date']         # Newest posts first
    paginate_by = 5                         # Number of posts per page

class PostDetailView(DetailView):
    """
    View to display a single blog post.
    Looks for 'pk' in the URL to identify the post.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # Access single post in template as {{ post }}

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new blog post.
    Only logged-in users can access this view.
    Automatically sets the logged-in user as the post author.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/'  # Redirect after successful creation

    def form_valid(self, form):
        # Automatically assign the current user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update an existing blog post.
    Only the original author can edit the post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = '/'  # Redirect after successful update

    def form_valid(self, form):
        # Keep the post author as the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Only allow access if current user is the author
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete an existing blog post.
    Only the original author can delete the post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('/')  # Redirect after successful deletion

    def test_func(self):
        # Only allow deletion if current user is the author
        post = self.get_object()
        return self.request.user == post.author
    
