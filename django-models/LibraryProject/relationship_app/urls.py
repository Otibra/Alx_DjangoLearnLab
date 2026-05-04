from django.urls import path
from .views import list_books, LibraryDetailView, register_view, home_view, logout_view
from django.contrib.auth.views import LoginView

urlpatterns =[
    path('books/', list_books, name='list_books'),

    # Class-based view: shows details of a single library
    # The <int:pk> is required because DetailView expects a primary key by default
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
]  
