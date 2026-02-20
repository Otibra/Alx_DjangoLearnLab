from django.urls import path
from . import views  # Import the views we created earlier

app_name = 'blog'  # Optional, for namespacing URLs

urlpatterns = [
    path('register/', views.register, name='register'),  # /register
    path('login/', views.user_login, name='login'),      # /login
    path('logout/', views.user_logout, name='logout'),   # /logout
    path('profile/', views.profile, name='profile'),     # /profile
]
