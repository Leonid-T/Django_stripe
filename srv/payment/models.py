from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.PositiveIntegerField()
