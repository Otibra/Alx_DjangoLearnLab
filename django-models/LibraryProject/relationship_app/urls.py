from django.urls import path, include

urlpatterns = [
    path('', include('relationship_app.urls')),
]
