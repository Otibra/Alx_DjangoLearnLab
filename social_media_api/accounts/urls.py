from django.urls import path

from .views import RegisterView, LoginView, ProfileView,FollowUserView, UnfollowUserView,FollowingView,FollowersView,UserFollowingView,UserFollowersView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "follow-user/<int:user_id>/follow/",
        FollowUserView.as_view(),
        name="follow-user",
    ),

    path(
        "unfollow-user/<int:user_id>/unfollow/",
        UnfollowUserView.as_view(),
        name="unfollow-user",
    ),

    path(
        "following/",
        FollowingView.as_view(),
        name="following",
    ),

    path(
        "followers/",
        FollowersView.as_view(),
        name="followers",
    ),

    path(
        "user-following/<int:user_id>/following/",
        UserFollowingView.as_view(),
        name="user-following",
    ),

    path(
        "users-followers/<int:user_id>/followers/",
        UserFollowersView.as_view(),
        name="user-followers",
    ),

]
