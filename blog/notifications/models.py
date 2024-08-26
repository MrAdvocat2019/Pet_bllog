from django.db import models

# Create your models here.
class Subscriber(models.Model):
    username = models.CharField()
    chat_id = models.CharField(unique=True)
