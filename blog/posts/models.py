import datetime
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    blog_text = models.TextField()
    number_likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='thumbnails/default.jpg')

    def get_short_info(self):
        text = self.blog_text

        a = text.split()[:20]
        return " ".join(a)