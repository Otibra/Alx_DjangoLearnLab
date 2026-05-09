from django.urls import path
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view
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
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]

