from django.urls import path

from . import views


urlpatterns = [

    # View notifications
    path(
        "notifications/",views.notifications_list, name="notifications_list"),
]