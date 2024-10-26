from django.db import models
from django.contrib.postgres.fields import ArrayField  # For PostgreSQL support (optional)
from Accommodation.models import Accommodation
from Flight.models import Flight
from RentalTransport.models import RentalTransport
from Event.models import Event

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    name_reservation = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True, null=True)
    cin = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField() 
    id_flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    id_accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    user_id = models.PositiveIntegerField(default=1)  
    id_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    
    # New status field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    number_of_travelers = models.PositiveIntegerField(default=1)

    # Field to store a list of passport numbers
    passport_numbers = models.JSONField(default=list, blank=True)  # Using JSONField to store the list

    def __str__(self):
        return f"Reservation: {self.name_reservation} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}, Status: {self.get_status_display()}"
