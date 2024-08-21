from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
    path("", views.about_page, name="about"),
]