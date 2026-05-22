from rest_framework import viewsets, permissions, generics
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from .utility import create_notification
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # users that current user follows
        following_users = user.following.all()

        # posts from followed users only
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)



@login_required
def unlike_post(request, post_id):
    """
    Allows an authenticated user to remove their like from a post.
    """

    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if not like:
        messages.warning(request, "You have not liked this post.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    like.delete()

    messages.success(request, "Post unliked successfully.")

    return redirect(request.META.get("HTTP_REFERER", "/"))

#notification for like


@login_required
def like_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if created:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            post=post
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        content = request.POST.get("content")

        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )

        # Create notification
        create_notification(
            recipient=post.author,
            actor=request.user,
            verb="commented on your post",
            target=comment
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))

#notification for follower

@login_required
def follow_user(request, user_id):

    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    # Prevent self-follow
    if user_to_follow == request.user:
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # toggle follow
    if request.user.following.filter(id=user_to_follow.id).exists():
        request.user.following.remove(user_to_follow)
    else:
        request.user.following.add(user_to_follow)

    return redirect(request.META.get("HTTP_REFERER", "/"))


    # Create notification
    create_notification(
        recipient=user_to_follow,
        actor=request.user,
        verb="started following you",
        target=follow
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))

#notification for login user

@login_required
def notifications_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("is_read", "-timestamp")

    unread_count = notifications.filter(
        is_read=False
    ).count()

    context = {
        "notifications": notifications,
        "unread_count": unread_count,
    }

    return render(
        request,
        "notifications/list.html",
        context
    )
