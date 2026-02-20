from django import forms
from django.contrib.auth.models import User

# Form to allow users to update their profile information (username and email)
class UserUpdateForm(forms.ModelForm):
    # Make email a required field
    email = forms.EmailField(required=True)

    class Meta:
        # Form is based on the built-in User model
        model = User
        # Only allow username and email to be updated
        fields = ['username', 'email']
        