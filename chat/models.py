from django.db import models
import datetime
from django.conf import settings
from django.utils.timezone import make_aware
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    naive_datetime = datetime.datetime.now()
    naive_datetime.tzinfo
    settings.TIME_ZONE  # 'UTC'
    aware_datetime = make_aware(naive_datetime)
    aware_datetime.tzinfo  # <UTC>
    date = models.DateTimeField(default=aware_datetime, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    image = models.CharField(max_length=1000000, blank=True)

