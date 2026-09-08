from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet,LikePostView, UnlikePostView
from django.urls import path 


router = DefaultRouter()

router.register(r"", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:post_id>/like/",
        LikePostView.as_view(),
        name="like",
    ),
    path(
        "posts/<int:post_id>/unlike/",
        UnlikePostView.as_view(),
        name="unlike",
    ),
]
