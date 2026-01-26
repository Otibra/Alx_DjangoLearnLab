from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Only users with role 'Admin' can access
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_dashboard.html', {'user': request.user})
