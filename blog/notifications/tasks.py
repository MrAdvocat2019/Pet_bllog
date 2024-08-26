import time
from celery import shared_task
from .models import Subscriber
from bot.bot import bot
@shared_task()
def messaging(title, pk):
    sub_list = Subscriber.objects.all()
    text = f"""Вышел новый пост с названием {title} посмотрите его по ссылке http://127.0.0.1:8000/posts/{pk}/
"""
    time.sleep(10)
    for sub in sub_list:
        chat_id = sub.chat_id
        bot.send_message(chat_id, text)