import datetime
from django.db import models

from .tasks import send_notification_1
from notifications.tasks import messaging
from categories.models import Category


class Post(models.Model):
    title = models.CharField(max_length=200)
    blog_text = models.TextField()
    number_likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', default='thumbnails/default.jpg')
    categories = models.ManyToManyField(Category)

    def get_short_info(self):
        text = self.blog_text

        a = text.split()[:20]
        return " ".join(a)

    def get_verbose_month(self):
        dict = {
            1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря',
        }
        try:
            return dict[self.pub_date.month]
        except:
            return "Wrong month"
    def save(self, *args, **kwargs):
        is_created = self.pk is None
        super(Post, self).save(*args, **kwargs)

        if is_created:
            # Convert the categories to a list of IDs
            messaging.delay(self.title, self.pk)

    
    def __str__(self):
        return self.title
