from django.db import models

class Flight(models.Model):
    flight_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='flight_images/', blank=True, null=True)  
    flight_number = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    airline = models.CharField(max_length=100)
    price_per_place = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"{self.flight_name} ({self.flight_number}) from {self.departure_city} to {self.arrival_city}"
