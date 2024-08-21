# urls.py
from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
    path("allposts/", views.AllPostsView.as_view(), name="all"),
]
