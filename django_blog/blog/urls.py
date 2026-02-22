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
    path('', views.PostListView.as_view(), name='blog-home'),

    # View a single post’s details
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # Create a new post
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),

    # Update a post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),

    # Delete a post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # About page
    path('about/', views.about, name='blog-about'),
]
