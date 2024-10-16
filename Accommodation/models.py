from django.db import models

class Accommodation(models.Model):
    TYPE_OF_ACCOMMODATION_CHOICES = (
        ("Hotel Room", "Hotel Room"),
        ("House", "House"),
        ("Apartment", "Apartment"),
        ("Villa", "Villa"),
    )

    AMENITIES_CHOICES = (
        ("Wi-Fi", "Wi-Fi"),
        ("Pool", "Pool"),
        ("Parking", "Parking"),
        ("Gym", "Gym"),
        ("Breakfast", "Breakfast"),
        ("Air Conditioning", "Air Conditioning"),
    )

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='accommodation_images/') 
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()
    type_of_accommodation = models.CharField(max_length=50, choices=TYPE_OF_ACCOMMODATION_CHOICES)  
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.CharField(max_length=200, choices=AMENITIES_CHOICES) 
    rating = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return f"{self.name} - {self.type_of_accommodation} in {self.city}"
