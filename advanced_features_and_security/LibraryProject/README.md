# Django Permissions & Groups Setup (Library Project)

## Overview

This project uses Django’s built-in authentication system with **custom permissions and groups** to control access to the `Book` model. Permissions are assigned to groups, and users inherit permissions through their group membership.


## Custom Model Permissions

The `Book` model defines the following custom permissions:

```python
class Meta:
    permissions = [
        ("can_view", "Can view book"),
        ("can_create", "Can create book"),
        ("can_edit", "Can edit book"),
        ("can_delete", "Can delete book"),
    ]
```

### Meaning of Permissions

| Permission   | Description                   |
| ------------ | ----------------------------- |
| `can_view`   | Allows viewing books          |
| `can_create` | Allows creating new books     |
| `can_edit`   | Allows editing existing books |
| `can_delete` | Allows deleting books         |


## User Groups

Three groups are used to manage access control:

### 1. Admins

* Full access to the system
* Permissions:

  * can_view
  * can_create
  * can_edit
  * can_delete

### 2. Editors

* Can manage content but cannot delete
* Permissions:

  * can_view
  * can_create
  * can_edit

### 3. Viewers

* Read-only access
* Permissions:

  * can_view


## Group and Permission Setup

Groups and permissions are created automatically after migrations using a **signal handler**:

### `signals.py`

* Runs after `post_migrate`
* Creates groups if they do not exist
* Assigns permissions to each group

```python
@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    admin_group, _ = Group.objects.get_or_create(name='Admins')
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    viewer_group, _ = Group.objects.get_or_create(name='Viewers')
```


## User Assignment

Users are assigned to groups like this:

```python
user.groups.add(admin_group)
```

Example users:

| Username    | Group   |
| ----------- | ------- |
| admin_user  | Admins  |
| editor_user | Editors |
| viewer_user | Viewers |


## Protecting Views

Views are protected using:

```python
@permission_required('bookshelf.can_edit', raise_exception=True)
```

### Example:

```python
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    ...
```

### Behavior:

* ✔ Allowed users → access granted
* ❌ Unauthorized users → 403 Forbidden


## Template Access Control

Permissions can also be used in templates:

```html
{% if perms.bookshelf.can_edit %}
    <a href="{% url 'edit_book' book.id %}">Edit</a>
{% endif %}
```


## Testing Permissions

Test users in Django shell:

```python
admin_user.has_perm('bookshelf.can_delete')  # True
editor_user.has_perm('bookshelf.can_delete') # False
viewer_user.has_perm('bookshelf.can_view')   # True
```


## Summary

* Permissions are defined in the `Book` model
* Groups manage sets of permissions
* Users inherit permissions through groups
* Views enforce permissions using decorators
* Templates use `perms` for UI control


