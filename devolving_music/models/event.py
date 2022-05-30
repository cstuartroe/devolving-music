from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()
    created_at = models.DateTimeField()
    image = models.CharField(max_length=128)
    visible = models.BooleanField()
