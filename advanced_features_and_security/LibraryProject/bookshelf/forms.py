from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 2:
            raise forms.ValidationError(
                "Title must contain at least 2 characters."
            )

        return title.strip()

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')

        if year < 0:
            raise forms.ValidationError(
                "Publication year cannot be negative."
            )

        return year
    