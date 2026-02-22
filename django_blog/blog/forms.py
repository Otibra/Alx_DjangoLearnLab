from django import forms
from django.contrib.auth.models import User
from .models import Post

# Form to allow users to update their profile information (username and email)
class UserUpdateForm(forms.ModelForm):
    # Make email a required field
    email = forms.EmailField(required=True)

    class Meta:
        # Form is based on the built-in User model
        model = User
        # Only allow username and email to be updated
        fields = ['username', 'email']
class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating Post objects.

    This form automatically generates form fields based on the Post model.
    The 'author' field is intentionally excluded because it is set
    automatically in the view using the logged-in user.
    """

    class Meta:
        model = Post
        # Only include fields that the user should fill in.
        # 'author' is excluded for security reasons.
        # 'published_date' is auto-generated.
        fields = ['title', 'content']       