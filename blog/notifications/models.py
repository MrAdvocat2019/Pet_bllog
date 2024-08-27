from django.db import models

from categories.models import Category

# Create your models here.
class Subscriber(models.Model):
    username = models.CharField()
    chat_id = models.CharField(unique=True)
    categories = models.ManyToManyField(Category)
