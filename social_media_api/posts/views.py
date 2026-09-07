from rest_framework import viewsets, permissions, filters

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .pagination import PostCommentPagination


class IsAuthorOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,permissions.IsAuthenticated]

    pagination_class = PostCommentPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,permissions.IsAuthenticated]

    pagination_class = PostCommentPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all().order_by("-created_at")

        post_id = self.request.query_params.get("post")

        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset
    