from django.db import models
from Accommodation.models import Accommodation
from Flight.models import Flight
from RentalTransport.models import RentalTransport
from Event.models import Event

class Reservation(models.Model):
    name_reservation = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_requests = models.TextField(blank=True, null=True)
    cin = models.PositiveIntegerField()

    class Meta:
        abstract = True  # Cette classe ne sera pas utilisée pour créer une table dans la base de données

class AccommodationReservation(Reservation):
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    night_numbers = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)  # Peut varier selon le format souhaité
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reservations')

class FlightReservation(Reservation):
    seat_class = models.CharField(max_length=50, choices=[
        ("Economic", "Economic"),
("Business", "Business"),
("First", "First"),
    ])
    seat_numbers = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')

class EventReservation(Reservation):
    seat_numbers = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')

class TransportReservation(Reservation):
    pickup_date = models.DateField()
    dropoff_date = models.DateField()
    nb_days = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)  # Peut varier selon le format souhaité
    rental_transport = models.ForeignKey(RentalTransport, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f"Transport Reservation for {self.name_reservation} on {self.pickup_date}"
