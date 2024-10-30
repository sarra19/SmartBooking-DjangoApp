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
    description = models.TextField()
    type_of_accommodation = models.CharField(max_length=50, choices=TYPE_OF_ACCOMMODATION_CHOICES)  
    price_per_night = models.DecimalField(max_digits=10, decimal_places=0)
    amenities = models.CharField(max_length=200, choices=AMENITIES_CHOICES) 
    ratings = models.JSONField(default=list)  # Pour stocker les évaluations individuelles
    rating = models.FloatField(null=True, blank=True)  # Pour stocker la note moyenne
    feedbacks = models.JSONField(default=list)  # Nouveau champ pour stocker les feedbacks
    city = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"{self.name} - {self.type_of_accommodation} in {self.location}"
    def update_rating(self, new_rating):
        self.ratings.append(new_rating)
        self.rating = sum(self.ratings) / len(self.ratings)  # Calcule la note moyenne
        self.save()
   
    def add_feedback(self, feedback, sentiment, score):
        feedback_entry = {
            "feedback": feedback,
            "sentiment": sentiment,
            "score": score,
        }
        self.feedbacks.append(feedback_entry)
        self.save()
        

    def feedback_statistics(self):
        positive_count = sum(1 for fb in self.feedbacks if fb.get("sentiment") == "positive")
        negative_count = sum(1 for fb in self.feedbacks if fb.get("sentiment") == "negative")
        neutral_count = sum(1 for fb in self.feedbacks if fb.get("sentiment") == "neutral")
        total = len(self.feedbacks)  # Use the length of the list

        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "total": total,
        }
    