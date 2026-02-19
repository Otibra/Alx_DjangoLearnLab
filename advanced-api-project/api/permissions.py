from rest_framework import permissions


class IsEditor(permissions.BasePermission):
    """
    Allows access only to users in the 'Editors' group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Editors').exists()
        )


class IsAdminUserCustom(permissions.BasePermission):
    """
    Allows access only to users in the 'Admins' group.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Admins').exists()
        )
