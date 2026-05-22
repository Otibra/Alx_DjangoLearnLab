# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Like, Notification


@login_required
def like_post(request, post_id):
    """
    Allows an authenticated user to like a post.
    Prevents duplicate likes and creates a notification.
    """

    post = get_object_or_404(Post, id=post_id)

    # Check if the user already liked the post
    already_liked = Like.objects.filter(
        user=request.user,
        post=post
    ).exists()

    if already_liked:
        messages.warning(request, "You already liked this post.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Create the like
    Like.objects.create(
        user=request.user,
        post=post
    )

    # Create notification
    # Prevent notifying yourself
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

    messages.success(request, "Post liked successfully.")

    return redirect(request.META.get("HTTP_REFERER", "/"))

