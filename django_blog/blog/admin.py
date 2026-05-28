from django.contrib import admin
from .models import Post, Comment, Tag  # add all your models here

# Register your models
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
