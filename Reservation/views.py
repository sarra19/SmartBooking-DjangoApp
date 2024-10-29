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
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template

import json
import requests
from django.http import JsonResponse
from django.conf import settings
import requests
import os
import google.generativeai as genai


import re
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

@csrf_exempt  # Use CSRF exemption for simplicity; adjust as needed
def generate_reservinfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        
        reservinfo = ai_generate_reservinfo(prompt)
        
        return JsonResponse(reservinfo)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

def ai_generate_reservinfo(prompt):
    if not isinstance(prompt, str) or not prompt.strip():
        return {'text': 'Error', 'message': 'Invalid input: prompt is required and must be a string.'}

    # Regular expressions to extract reservation details without commas
    name_reservation = re.search(r"my name is\s*([\w\s]+)", prompt, re.IGNORECASE)
    cin = re.search(r"my CIN is\s*(\d+)", prompt, re.IGNORECASE)
    phone_number = re.search(r"my phone number is\s*(\d+)", prompt, re.IGNORECASE)
    special_requests = re.search(r"special request\s*:\s*(.+)", prompt, re.IGNORECASE)

    reservation_data = {
        'name_reservation': name_reservation.group(1) if name_reservation else 'Unknown',
        'cin': cin.group(1) if cin else 'Unknown',
        'phone_number': phone_number.group(1) if phone_number else 'Unknown',
        'special_requests': special_requests.group(1) if special_requests else 'None'
    }

    return {
        'text': 'Reservation generated.',
        'message': 'Reservation successfully added.',
        'reservinfo': "Reservation Info Generated",  # Placeholder for any generated info
        'reservation_details': reservation_data
    }

class RsvEventFront(ListView):
    model = Event  #
    context_object_name = "events"  
    template_name = 'frontOffice/pages/Event/index.html'  
    
    def get_queryset(self):
        # Fetch and order all events by ID
        events = Event.objects.all().order_by('id')
        return events

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
        passport_numbers = self.request.POST.getlist('passport_numbers[]')
        reservation = form.save(commit=False)
        reservation.status = self.request.POST.get('status', 'pending') or 'pending'

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
    form_class = ReservationForm
    success_url = reverse_lazy("reservation:Rsv")

    def form_valid(self, form):
        # First, save the reservation instance but don't commit yet
        reservation = form.save(commit=False)

        # Process passport numbers from the request
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        # Update the passport_numbers field with the new list
        reservation.passport_numbers = passport_numbers  # Save the list directly

        # Now save the reservation
        reservation.save()

        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the reservation. Please check the details and try again.")
        return super().form_invalid(form)

class UpdateReservationfView(UpdateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/update.html'
    form_class = ReservationForm
    #userid
    success_url = reverse_lazy('reservation:myreservation', args=[1]) 

    def form_valid(self, form):
        # First, save the reservation instance but don't commit yet
        reservation = form.save(commit=False)

        # Process passport numbers from the request
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        # Update the passport_numbers field with the new list
        reservation.passport_numbers = passport_numbers  # Save the list directly

        # Now save the reservation
        reservation.save()

        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the reservation. Please check the details and try again.")
        return super().form_invalid(form)


class UpdateReservationEventView(UpdateView):
    model = Reservation
    template_name = 'backOffice/pages/Reservation/updateEvent.html'
    form_class = ReservationForm
    success_url = reverse_lazy("reservation:Rsv")

    def form_valid(self, form):
        # First, save the reservation instance but don't commit yet
        reservation = form.save(commit=False)

        # Process passport numbers from the request
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        # Update the passport_numbers field with the new list
        reservation.passport_numbers = passport_numbers  # Save the list directly

        # Now save the reservation
        reservation.save()

        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the reservation. Please check the details and try again.")
        return super().form_invalid(form)

class UpdateReservationEventfView(UpdateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/updateEventf.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:myreservation', args=[1])

    def form_valid(self, form):
        # First, save the reservation instance but don't commit yet
        reservation = form.save(commit=False)

        # Process passport numbers from the request
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        # Update the passport_numbers field with the new list
        reservation.passport_numbers = passport_numbers  # Save the list directly

        # Now save the reservation
        reservation.save()

        messages.success(self.request, "Flight reservation updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the reservation. Please check the details and try again.")
        return super().form_invalid(form)

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
        flight_id = self.kwargs.get('pk') 
        accommodation_id = self.kwargs.get('ak')  
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        reservation = form.save(commit=False)

        reservation.id_flight_id = flight_id 
        reservation.id_accommodation_id = accommodation_id if accommodation_id and accommodation_id != '0' else None
        reservation.passport_numbers = passport_numbers if passport_numbers and passport_numbers != '0' else None

        
        reservation.save()
        
        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

# Displays a list of reservations for a specific user, paginated
class my_reservations(ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "frontOffice/pages/Reservation/index.html"
    paginate_by = 6

    def get_queryset(self):
        # Retrieve user-specific reservations
        pk = self.kwargs.get('pk')
        queryset = Reservation.objects.filter(user_id=pk)

        # Filtering by search query
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
            ) | queryset.filter(
                passport_numbers__icontains=search_query  # Updated to use __icontains
            )

        # Filtering by reservation status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Sorting by specified field, defaulting to 'created_at'
        sort_field = self.request.GET.get('sort', 'created_at')
        valid_sort_fields = ['name_reservation', 'cin', 'phone_number', 'created_at']
        if sort_field in valid_sort_fields:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('created_at')

        return queryset

# Deletes a reservation for the front-end user view
class delete_freservation(DeleteView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/delete.html'
    
    success_url = reverse_lazy('reservation:myreservation', args=[1])




class AddRsvEventfront(CreateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/addREvent.html'
    form_class = ReservationForm
    #userid
    success_url = reverse_lazy('reservation:myreservation', args=[1])  #userid

    def form_valid(self, form):
        event_id = self.kwargs['ek']  
        reservation = form.save(commit=False)
        reservation.id_event = get_object_or_404(Event, id=event_id) 
        reservation.save()

        messages.success(self.request, "Reservation added successfully!")  
        return super().form_valid(form)

   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['ek']
        context['event'] = get_object_or_404(Event, id=event_id)  
        return context
    


        
def accept_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    
    reservation.status = 'accepted'
    
    if reservation.id_accommodation:
        accommodation = reservation.id_accommodation  
        accommodation_id = accommodation.id  

        accommodation.delete()  
        reservation.id_accommodation = None 
        messages.success(request, f'Accommodation with ID {accommodation_id} has been deleted.')

    reservation.save()
    messages.success(request, 'Reservation accepted successfully.')
    return redirect('reservation:Rsv')  

def reject_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'rejected'
    reservation.save()
    messages.success(request, 'Reservation rejected successfully.')
    return redirect('reservation:Rsv') 


class RsvAccommodationFront(ListView):
    model=Accommodation
    context_object_name="accommodations"
    
    template_name='frontOffice/pages/Accommodation/indexAll.html'
    
    def get_queryset(self):
        
        accommodations = Accommodation.objects.all().order_by('id')
        
        return accommodations
    

class AddRsvfrontAcc(CreateView):
    model = Reservation
    template_name = 'frontOffice/pages/Reservation/add.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation:myreservation', args=[1])

    def form_valid(self, form):
        accommodation_id = self.kwargs.get('ack')  
        passport_numbers = self.request.POST.getlist('passport_numbers[]')

        reservation = form.save(commit=False)

        reservation.id_accommodation_id = accommodation_id
        reservation.passport_numbers = passport_numbers if passport_numbers and passport_numbers != '0' else None

        
        reservation.save()
        
        messages.success(self.request, "Reservation added successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

def reservations_pdf(request):
    reservations = Reservation.objects.all()  # or any filtered queryset based on your requirement
    template_path = 'backOffice/pages/Reservation/reservations_list_pdf.html'  # New HTML template for the PDF
    context = {'reservations': reservations}

    # Render HTML to a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reservations_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with generating your PDF <pre>' + html + '</pre>')
    return response