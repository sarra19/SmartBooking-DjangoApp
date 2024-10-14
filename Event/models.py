from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/')  
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    price_per_place = models.DecimalField(max_digits=10, decimal_places=2)
    number_places = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)  # True: Available, False: Not Available

    def __str__(self):
        return f"{self.title} in {self.city} at {self.location}"
