from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Used for showing success or info messages
from django.contrib.auth.decorators import login_required  # Protects views from anonymous users
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from .forms import UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import forms


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

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Make sure you have a login URL
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')  # Redirect to profile after login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# Logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def about(request):
    return render(request, 'blog/about.html')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

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
    
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()

    return render(request, 'comments/comment_form.html', {'form': form})

def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/comment_form.html', {'form': form})


def clean_content(self):
    content = self.cleaned_data.get('content').strip()

    forbidden_words = ['spam', 'fake', 'scam']
    for word in forbidden_words:
        if word in content.lower():
            raise forms.ValidationError("Your comment contains inappropriate language.")

    return content

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
 # blog/views.py
def home(request):
    return render(request, 'blog/home.html') 

def posts(request):
    return render(request, 'posts.html') 