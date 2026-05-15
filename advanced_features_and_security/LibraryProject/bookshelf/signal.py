from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):

    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Admins')
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    viewer_group, _ = Group.objects.get_or_create(name='Viewers')

    # Get permissions
    permissions = Permission.objects.filter(
        codename__in=[
            'can_view',
            'can_create',
            'can_edit',
            'can_delete'
        ]
    )

    # Assign permissions
    for permission in permissions:

        if permission.codename in ['can_view', 'can_create', 'can_edit', 'can_delete']:
            admin_group.permissions.add(permission)

        if permission.codename in ['can_view', 'can_create', 'can_edit']:
            editor_group.permissions.add(permission)

        if permission.codename == 'can_view':
            viewer_group.permissions.add(permission)
            