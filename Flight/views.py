from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight
from .forms import FlightForm
from django.urls import reverse
from django.db.models import Q  # Ajoute cette ligne pour importer Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Importer les classes nécessaires
import requests
from django.shortcuts import render
from amadeus import Client, ResponseError
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet





def download_flights_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="flights.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)

    flights = Flight.objects.all()

    data = [['Image', 'Airline', 'Flight Name', 'Flight Number', 'Departure City', 'Arrival City', 'Departure Date', 'Arrival Date', 'Price Per Place']]
    
    for flight in flights:
        image_path = flight.image.path if flight.image else None
        image = Image(image_path, width=0.5 * inch, height=0.5 * inch) if image_path else "No Image"
        
        data.append([
            image,
            flight.airline,
            flight.flight_name,
            flight.flight_number,
            flight.departure_city,
            flight.arrival_city,
            flight.departure_date.strftime('%Y-%m-%d'),  
            flight.arrival_date.strftime('%Y-%m-%d'),    
            f"{flight.price_per_place} DT"
        ])

    column_widths = [0.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch]
    table = Table(data, colWidths=column_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    styles = getSampleStyleSheet()
    title = Paragraph("List of Flights", styles['Title'])

    elements = [title, table]
    pdf.build(elements)

    return response





# Liste des vols
# def flight_list(request):
#     flights = Flight.objects.all()  # Get all flights from the database
#     context = {
#         'flights': flights,
#     }
#     return render(request, 'BackOffice/Flights/index.html', context)
# Fonction pour obtenir des recommandations de vols depuis l'API Gemini


def flight_list(request):
    flights = Flight.objects.all()

    search_query = request.GET.get('q', '')
    if search_query:
        flights = flights.filter(
            Q(flight_name__icontains=search_query) |
            Q(flight_number__icontains=search_query) |
            Q(departure_city__icontains=search_query) |
            Q(arrival_city__icontains=search_query)  
        )

    sort_by = request.GET.get('sort')  
    valid_sort_fields = [
  'departure_date', 'arrival_date', 'flight_number', 'price_per_place' 

    ]

    if sort_by in valid_sort_fields:
        flights = flights.order_by(sort_by)
    else:
        flights = flights.order_by('departure_date')  

    # Pagination
    paginator = Paginator(flights, 3) 
    page_number = request.GET.get('page')  
    try:
        flights_page = paginator.page(page_number)  
    except PageNotAnInteger:
        flights_page = paginator.page(1)  
    except EmptyPage:
        flights_page = paginator.page(paginator.num_pages)  
 

    context = {
        'flights': flights_page,  
        'sort_by': sort_by,
        'search_query': search_query,  
        'page_obj': flights_page,  
        'is_paginated': paginator.num_pages > 1, 


    }

    return render(request, 'BackOffice/Flights/index.html', context)




def flight_list_front(request):

    flights = Flight.objects.all()

    context = {
        'flights': flights,
                # 'popular_flights': popular_flights,

    }

    return render(request, 'FrontOffice/Flights/index.html', context)



# def flight_detail(request, flight_id):
#     flight = get_object_or_404(Flight, id=flight_id)
#     context = {
#         'flight': flight
#     }
#     return render(request, 'frontOffice/flight_detail.html', context)  # Changez le chemin en fonction de l'emplacement de votre template


# Détail d'un vol
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(request, 'flight/flight_detail.html', {'flight': flight})

# Créer un vol
def flight_create(request):
    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Flight:flight_list') 
    else:
        form = FlightForm()
    return render(request, 'BackOffice/Flights/create.html', {'form': form})

# Modifier un vol
def flight_update(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('Flight:flight_list')  # Redirige vers la liste des vols après la mise à jour
    else:
        form = FlightForm(instance=flight)  # Prend les données existantes pour pré-remplir le formulaire

    return render(request, 'BackOffice/Flights/update.html', {'flight': flight, 'form': form})
    
# Supprimer un vol
def flight_delete(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        flight.delete()
        return redirect('Flight:flight_list')  # Utilise 'Flight:flight_list'
    return render(request, 'flight/flight_confirm_delete.html', {'flight': flight})
