from django.db import models

class RentalTransport(models.Model):
    TRANSPORT_TYPE_CHOICES = (
        ("Car", "Car"),
        ("Bike", "Bike"),
        ("Scooter", "Scooter"),
        ("Motorbike", "Motorbike"),
    )

    VEHICLE_MODEL_CHOICES = (
        ("Toyota Corolla", "Toyota Corolla"),
        ("Honda Civic", "Honda Civic"),
        ("Ford Fiesta", "Ford Fiesta"),
        ("BMW 3 Series", "BMW 3 Series"),
        ("Kawasaki Ninja", "Kawasaki Ninja"),
    )

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='rental_images/')  
    transport_type = models.CharField(max_length=50, choices=TRANSPORT_TYPE_CHOICES)  
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_model = models.CharField(max_length=100, choices=VEHICLE_MODEL_CHOICES)  
    vehicle_capacity = models.PositiveIntegerField()  
    def __str__(self):
        return f"{self.title} ({self.transport_type}) - {self.vehicle_model} in {self.city}"
