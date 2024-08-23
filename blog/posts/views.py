# views.py
from django.utils import timezone
from django.core.paginator import Paginator
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from categories.models import Category


from .models import Post

def list_view(request:HttpRequest):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 8) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    cats = None
    if request.GET.getlist('categories'):
        cats = request.GET.getlist('categories')
        for c in cats:
            posts_list = posts_list.filter(categories__pk=int(c))  
    paginator = Paginator(posts_list, 6) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/allposts.html', {"page_obj":page_obj, "posts_list":posts_list,'Category':categories, 'selected_categories':cats})
class AllPostsView(generic.ListView):
    template_name = "posts/allposts.html"
    paginate_by = 6
    context_object_name = 'posts_list'
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(pub_date__lte=timezone.now())