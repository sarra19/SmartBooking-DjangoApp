from django.db import models
from Accommodation.models import Accommodation  

class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    price_per_place = models.DecimalField(max_digits=10, decimal_places=2)
    number_places = models.PositiveIntegerField()
    accommodation = models.ForeignKey(Accommodation,  on_delete=models.SET_NULL, null=True, blank=True, related_name='events')

    def __str__(self):
        return f"{self.title} in {self.city} at {self.location}"
