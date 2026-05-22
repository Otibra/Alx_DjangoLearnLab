from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PostViewSet, CommentViewSet, FeedView, like_post, unlike_post

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),  # include router endpoints
    path("feed/", FeedView.as_view(), name="feed"),
    path("posts/<int:pk>/like/",like_post,name="like_post"),
    path("posts/<int:pk>/unlike/",unlike_post,name="unlike_post"),
]
