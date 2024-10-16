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

class Rsv(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'backOffice/pages/Reservation/index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Reservation.objects.all()

        # Search functionality
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
                id_transport__id__icontains=search_query 
            ) | queryset.filter(
                special_requests__icontains=search_query
            ) | queryset.filter(
                phone_number__icontains=search_query 
            )

        sort_field = self.request.GET.get('sort', 'id') 
        valid_sort_fields = [
            'name_reservation', 'cin', 'phone_number',
            'id_flight__id', 'id_accommodation__id', 'id_transport__id', 'id'
        ]

        if sort_field in valid_sort_fields:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('id')  

        return queryset



def add_reservation(request):
    form = ReservationForm()
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservation:Rsv")

    return render(request, "backOffice/pages/Reservation/add.html", {'form': form})

class AddReservationView(CreateView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:Rsv')  

    def form_valid(self, form):
        messages.success(self.request, "reservation added successfully!")
        return super().form_valid(form)


class delete_reservation(DeleteView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/delete.html'
    
    success_url=reverse_lazy("reservation:Rsv")



class UpdateReservationView(UpdateView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/update.html'
    form_class=ReservationForm

    success_url=reverse_lazy("reservation:Rsv")
    def form_valid(self, form):
        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)




def detailsReservation(request, pk):
    
    reservation = Reservation.objects.get(id=pk)
    
   
  
    
    return render(request,"backOffice/pages/Reservation/details.html",{"reservation":reservation})

# front
class RsvFlightFront(ListView):
    model=Flight
    context_object_name="flights"
    
    template_name='frontOffice/pages/Flight/index.html'
    
    def get_queryset(self):
        
        flights = Flight.objects.all().order_by('id')
        
        return flights

class RsvAccfront(ListView):
    model = Accommodation
    context_object_name = "accommodations"
    template_name = 'frontOffice/pages/Accommodation/index.html'
    
    def get_queryset(self):
        # You can customize the queryset here if needed
        return Accommodation.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        
        # Get the flight_id from the URL and add it to the context
        flight_id = self.kwargs.get('pk')  # Adjust this based on your URL pattern
        context['flight_id'] = flight_id
        
        return context


class RsvTrsfront(ListView):
    model = RentalTransport
    context_object_name = "transports"
    template_name = 'frontOffice/pages/RentalTransport/index.html'
    
    def get_queryset(self):
        # You can customize the queryset here if needed
        return RentalTransport.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        
        # Get the flight_id and accommodation_id from the URL and add them to the context
        flight_id = self.kwargs.get('pk')  # Flight ID
        accommodation_id = self.kwargs.get('ak', None)  # Accommodation ID, default to None if not provided
        
        context['flight_id'] = flight_id
        context['accommodation_id'] = accommodation_id 
        
        return context


class AddRsvfront(CreateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:Rsv-flight-front')

    def form_valid(self, form):
        flight_id = self.kwargs['pk']  # Flight ID
        accommodation_id = self.kwargs.get('ak')  
        transport_id = self.kwargs.get('tk')  # Transport ID, defaults to None
        
        # Create the reservation object but do not save it yet
        reservation = form.save(commit=False)
        
        # Set to None if the values are 0
        flight_id = None if flight_id == 0 else flight_id
        accommodation_id = None if accommodation_id == 0 else accommodation_id
        transport_id = None if transport_id == 0 else transport_id

        # Assign the foreign key fields
        reservation.id_flight_id = flight_id
        reservation.id_accommodation_id = accommodation_id 
        reservation.id_transport_id = transport_id 
        
        # Now save the reservation object
        reservation.save()

        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)

class my_reservations(ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "frontOffice/pages/Reservation/index.html"
    paginate_by = 6

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        
        # Check if a reservation exists for the provided pk and user_id
        return Reservation.objects.filter(user_id=pk).order_by('created_at')

class delete_freservation(DeleteView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/delete.html'
    
    success_url=reverse_lazy("reservation:Rsv-flight-front") #a modifier?


        