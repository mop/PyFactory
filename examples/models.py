from django.db import models

class User(models.Model):
    name    = models.CharField(max_length = 50)
    url     = models.URLField()
    network = models.CharField(max_length = 50)
    reviews = models.ManyToManyField(Trackable, through='Review')
