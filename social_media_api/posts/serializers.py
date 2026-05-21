from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "comments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value
    