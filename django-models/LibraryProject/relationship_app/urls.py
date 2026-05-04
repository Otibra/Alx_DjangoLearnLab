from django.urls import path
from .views import list_books, LibraryDetailView
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns =[
    path('books/', list_books, name='list_books'),

    # Class-based view: shows details of a single library
    # The <int:pk> is required because DetailView expects a primary key by default
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home_view, name='home'),
]  
