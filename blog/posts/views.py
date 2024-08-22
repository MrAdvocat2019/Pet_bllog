# views.py
from django.utils import timezone
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Post

class AllPostsView(generic.ListView):
    template_name = "posts/allposts.html"
    paginate_by = 9
    context_object_name = 'posts_list'
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(pub_date__lte=timezone.now())