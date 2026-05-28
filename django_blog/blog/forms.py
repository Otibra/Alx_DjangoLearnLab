from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Tag



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



# forms.py

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'class': 'form-control'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')

        # Remove leading/trailing whitespace
        content = content.strip()

        # Validation rules
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")

        if len(content) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")

        if len(content) > 1000:
            raise forms.ValidationError("Comment cannot exceed 1000 characters.")

        return content      
    