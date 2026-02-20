from django.shortcuts import render, redirect
from django.contrib import messages  # For flash messages to show feedback to users
from django.contrib.auth.decorators import login_required  # To protect views for logged-in users
from django.contrib.auth.forms import AuthenticationForm  # Built-in form for login
from django.contrib.auth import login, logout  # Functions to log users in and out
from .forms import UserRegisterForm  # Custom registration form extending UserCreationForm

# -------------------------
# Registration View
# -------------------------
def register(request):
    """
    Handles user registration.
    Steps:
    1. If the request method is POST, a form is submitted by the user.
    2. Create a UserRegisterForm instance with the submitted data.
    3. Validate the form.
       - If valid, save the new user to the database.
       - Show a success message.
       - Redirect the user to the login page.
    4. If GET request, show an empty registration form.
    5. Render the registration template with the form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            username = form.cleaned_data.get('username')  # Get the username for a success message
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegisterForm()  # Empty form for GET request
    return render(request, 'users/register.html', {'form': form})

# -------------------------
# Login View
# -------------------------
def user_login(request):
    """
    Handles user login.
    Steps:
    1. If the request method is POST, the user submitted login credentials.
    2. Instantiate AuthenticationForm with the submitted data.
    3. Validate the form:
       - If valid, log the user in using Django's login() function.
       - Show a welcome message.
       - Redirect to profile page.
    4. If GET request, show an empty login form.
    5. Render the login template with the form.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            login(request, user)     # Log the user in
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
    else:
        form = AuthenticationForm()  # Empty login form for GET request
    return render(request, 'users/login.html', {'form': form})

# -------------------------
# Logout View
# -------------------------
@login_required
def user_logout(request):
    """
    Handles user logout.
    Steps:
    1. Only accessible to logged-in users (@login_required decorator).
    2. Calls Django's logout() function to end the user session.
    3. Show an informational message that the user has logged out.
    4. Redirect to login page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# -------------------------
# Profile View
# -------------------------
@login_required
def profile(request):
    """
    Displays the user profile.
    Steps:
    1. Only accessible to logged-in users.
    2. Pass the current user to the template using the built-in 'user' context variable.
    3. Render the profile template showing username and email.
    """
    return render(request, 'users/profile.html')
