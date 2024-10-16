from django.db import models
from Accommodation.models import Accommodation
from Flight.models import Flight
from RentalTransport.models import RentalTransport
from Event.models import Event

class Reservation(models.Model):
    name_reservation = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True, null=True)
    cin = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField() 
    id_flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    id_accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    id_transport = models.ForeignKey(RentalTransport, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    user_id = models.PositiveIntegerField(default=1)  

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Reservation: {self.name_reservation} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
