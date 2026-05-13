from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.models import Group, Permission


# Author Model
# ----------------------
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# Book Model
# ----------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )

    def __str__(self):
        return self.title

# Library Model
# ----------------------
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# Librarian Model
# ----------------------
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#........user profile.......
class UserProfile(models.Model):
    ROLE_CHOICES = [
         ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email=None,
        password=None,
        date_of_birth=None,
        profile_photo=None,
        **extra_fields
    ):
        """
        Create and return a regular user.
        """

        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username,
        email=None,
        password=None,
        date_of_birth=None,
        profile_photo=None,
        **extra_fields
    ):
        """
        Create and return a superuser.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )

class CustomUser(AbstractUser):
    # Add extra fields here
    date_of_birth = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to="UserProfile/", blank=True, null=True)

    objects = CustomUserManager()

   

    def __str__(self):
        return self.username
