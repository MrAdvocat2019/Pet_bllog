# views.py
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post

def all_posts(request):
    posts_list = Post.objects.all()
    context = {"posts_list": posts_list}
    return render(request, "posts/allposts.html", context=context)
class AllPostsView(generic.ListView):
    template_name = "posts/allposts.html"
    context_object_name = 'posts_list'
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.all()
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'