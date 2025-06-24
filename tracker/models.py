from django.db import models

class Bus(models.Model):
    number = models.CharField(max_length=10, unique=True)
    current_lat = models.FloatField()
    current_lng = models.FloatField()

    def __str__(self):
        return self.number
