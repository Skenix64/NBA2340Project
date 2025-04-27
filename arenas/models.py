from django.db import models

class Arena(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
