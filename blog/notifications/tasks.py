import time
from celery import shared_task
from django.apps import apps
from .models import Subscriber
from bot.bot import bot

def have_common_category(post, subscriber):
    return post.categories.filter(id__in=subscriber.categories.values('id')).exists()

@shared_task()
def messaging(title, pk):
    Post = apps.get_model('posts', 'Post')
    sub_list = Subscriber.objects.all()
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    text = f"""Вышел новый пост с названием {title} посмотрите его по ссылке http://127.0.0.1:8000/posts/{pk}/
"""
    for sub in sub_list:
        chat_id = sub.chat_id
        s = categories.intersection(sub.categories.all())
        if s.exists():
            bot.send_message(chat_id, text)
        