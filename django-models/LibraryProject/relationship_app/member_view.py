from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Only users with role 'Member' can access
def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_dashboard.html', {'user': request.user})
