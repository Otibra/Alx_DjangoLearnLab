from django.urls import path
from . import views  # Import the views we created earlier
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

app_name = 'blog'  # Optional, for namespacing URLs

urlpatterns = [
    path('register/', views.register, name='register'),  # /register
    path('login/', views.user_login, name='login'),      # /login
    path('logout/', views.user_logout, name='logout'),   # /logout
    path('profile/', views.profile, name='profile'),     # /profile
    # List all posts — accessible to everyone
    path('posts/', PostListView.as_view(), name='post-list'),


    # View a single post’s details
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Create a new post — authenticated users only
    path('posts/new/', PostCreateView.as_view(), name='post-create'),

    # Edit a post — only the author can edit
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),

    # Delete a post — only the author can delete
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
