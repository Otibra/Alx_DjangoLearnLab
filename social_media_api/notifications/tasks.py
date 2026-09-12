from celery import shared_task

from posts.models import Post
from notifications.utils import create_notification


@shared_task
def notify_followers(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return

    followers = post.author.followers.all()

    for follower in followers:
        create_notification(
            recipient=follower,
            actor=post.author,
            verb="created a new post",
            target=post,
        )
