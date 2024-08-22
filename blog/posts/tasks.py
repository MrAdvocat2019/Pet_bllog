import time
from celery import shared_task

@shared_task()
def send_notification_1():
    time.sleep(20)
    with open("text.txt", 'w') as f:
        f.write("executed125") 