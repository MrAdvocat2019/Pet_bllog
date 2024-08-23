# views.py
import datetime
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
    posts_list = Post.objects.filter(pub_date__lte=timezone.now())
    categories = Category.objects.all()
    cats = None

    #getting filtered by categories
    if request.GET.getlist('categories'):
        cats = request.GET.getlist('categories')
        for c in cats:
            posts_list = posts_list.filter(categories__pk=int(c))
            print (posts_list)
    print(request.GET.getlist('categories'))
    #getting filtered by dates
    date_start = '1970-01-01'
    date_finish = timezone.now()
    date_finish = f'{date_finish.year}-{date_finish.month}-{date_finish.day}'
    if request.GET.get('date_start'):
        date_start = request.GET.get('date_start').strip()
    if request.GET.get('date_finish'):
        date_finish = request.GET.get('date_finish').strip()
        

    date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')

    date_finish = datetime.datetime.strptime(date_finish, '%Y-%m-%d')
    date_finish = datetime.datetime(date_finish.year, date_finish.month, date_finish.day, 23,59,59)

    posts_list = posts_list.filter(pub_date__gte=date_start).filter(pub_date__lte=date_finish)
    print(posts_list)
    date_start = f'{date_start.year}-{str(date_start.month).zfill(2)}-{str(date_start.day).zfill(2)}'.strip()
    date_finish = f'{date_finish.year}-{str(date_finish.month).zfill(2)}-{str(date_finish.day).zfill(2)}'.strip()

    #paginating
    paginator = Paginator(posts_list, 6) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    len_post = len(posts_list)

    return render(request, 'posts/allposts.html', {"page_obj":page_obj, "posts_list":posts_list,'Category':categories, 'selected_categories':cats, 'date_start':date_start, 'date_finish':date_finish, 'len':len_post })
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