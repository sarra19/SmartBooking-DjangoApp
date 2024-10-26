from django.shortcuts import render, redirect 
from Reservation.models import Reservation
from Flight.models import Flight 
from Accommodation.models import Accommodation  
from RentalTransport.models import RentalTransport  
from Reservation.forms import ReservationForm
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from Event.models import Event 

# Displays a paginated list of reservations with search and sort options
class Rsv(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'backOffice/pages/Reservation/index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Reservation.objects.all()

        # Filter by search query
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = queryset.filter(
                name_reservation__icontains=search_query
            ) | queryset.filter(
                cin__icontains=search_query
            ) | queryset.filter(
                id_flight__id__icontains=search_query  
            ) | queryset.filter(
                id_accommodation__id__icontains=search_query  
            ) | queryset.filter(
                special_requests__icontains=search_query
            ) | queryset.filter(
                phone_number__icontains=search_query 
            )

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        # Sort by the specified field
        sort_field = self.request.GET.get('sort', 'id') 
        valid_sort_fields = [
            'name_reservation', 'cin', 'phone_number',
            'id_flight__id', 'id_accommodation__id', 'id'
        ]

        if sort_field in valid_sort_fields:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('id')  

        return queryset


# Renders a form to create a new reservation and saves it if valid
def add_reservation(request):
    form = ReservationForm()
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservation:Rsv")

    return render(request, "backOffice/pages/Reservation/add.html", {'form': form})

# Displays a form to create a new reservation using Django's CreateView
class AddReservationView(CreateView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:Rsv')  

    def form_valid(self, form):
        # Extract passport numbers from the request
        passport_numbers = self.request.POST.getlist('passport_numbers[]')
        reservation = form.save(commit=False)
        reservation.passport_numbers = passport_numbers  # Assuming you have a field for this in your model
        reservation.save()
        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)

# Deletes a reservation record
class delete_reservation(DeleteView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/delete.html'
    
    success_url=reverse_lazy("reservation:Rsv")


# Updates an existing reservation record
class UpdateReservationView(UpdateView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/update.html'
    form_class=ReservationForm

    success_url=reverse_lazy("reservation:Rsv")
    def form_valid(self, form):
        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)



# Displays the details of a specific reservation
def detailsReservation(request, pk):
    
    reservation = Reservation.objects.get(id=pk)
    
   
  
    
    return render(request,"backOffice/pages/Reservation/details.html",{"reservation":reservation})

#********************************************************************front**************************************************************

# Displays a list of available flights  (flight list)
class RsvFlightFront(ListView):
    model=Flight
    context_object_name="flights"
    
    template_name='frontOffice/pages/Flight/index.html'
    
    def get_queryset(self):
        
        flights = Flight.objects.all().order_by('id')
        
        return flights

# Displays a list of available accommodations, linked to a selected flight  (acco list)
class RsvAccfront(ListView): 
    model = Accommodation
    context_object_name = "accommodations"
    template_name = 'frontOffice/pages/Accommodation/index.html'
    
    def get_queryset(self):
        flight_id = self.kwargs.get('pk')  # Get the flight ID from the URL
        flight = Flight.objects.get(id=flight_id)  # Fetch the flight object
        
        # Filter accommodations by city name of the flight
        return Accommodation.objects.filter(city=flight.arrival_city).order_by('id')  # Ensure 'city' is the correct field name in your Accommodation model
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        flight_id = self.kwargs.get('pk')  
        context['flight_id'] = flight_id
        
        return context

# Renders a form to create a reservation for a specific flight and accommodation
class AddRsvfront(CreateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:myreservation', args=[1])

    def form_valid(self, form):
        flight_id = self.kwargs['pk']  # Flight ID
        accommodation_id = self.kwargs.get('ak')  
        
        reservation = form.save(commit=False)
        
        flight_id = None if flight_id == 0 else flight_id
        accommodation_id = None if accommodation_id == 0 else accommodation_id

        reservation.id_flight_id = flight_id
        reservation.id_accommodation_id = accommodation_id 
        
        reservation.save()

        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)

# Displays a list of reservations for a specific user, paginated
class my_reservations(ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "frontOffice/pages/Reservation/index.html"
    paginate_by = 6

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        
        return Reservation.objects.filter(user_id=pk).order_by('created_at')

# Deletes a reservation for the front-end user view
class delete_freservation(DeleteView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/delete.html'
    
    success_url = reverse_lazy('reservation:myreservation', args=[1])


class RsvEventFront(ListView):
    model = Event  #
    context_object_name = "events"  
    template_name = 'frontOffice/pages/Event/index.html'  
    
    def get_queryset(self):
        # Fetch and order all events by ID
        events = Event.objects.all().order_by('id')
        return events

class AddRsvEventfront(CreateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/addREvent.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:myreservation', args=[1])

    def form_valid(self, form):
        event_id = self.kwargs['ek']  # Flight ID
        reservation = form.save(commit=False)

        
       
        reservation.id_event_id= event_id
        reservation.save()

        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)


def accept_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    
    # Accept the reservation
    reservation.status = 'accepted'
    
    # Check if there is an associated accommodation
    if reservation.id_accommodation:
        accommodation = reservation.id_accommodation  # Get the accommodation object
        accommodation_id = accommodation.id  # Store the accommodation ID for messages
        # Delete the associated accommodation
        accommodation.delete()  # This deletes the accommodation object
        reservation.id_accommodation = None  # Clear the reference to the deleted accommodation
        messages.success(request, f'Accommodation with ID {accommodation_id} has been deleted.')

    # Save the changes to the reservation
    reservation.save()
    messages.success(request, 'Reservation accepted successfully.')
    return redirect('reservation:Rsv')  # Redirect to the reservations list

def reject_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'rejected'
    reservation.save()
    messages.success(request, 'Reservation rejected successfully.')
    return redirect('reservation:Rsv')  # Redirect to the reservations lis