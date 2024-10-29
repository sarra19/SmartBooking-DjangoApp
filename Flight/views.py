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
    # Créer un objet HttpResponse avec le type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="flights.pdf"'

    # Créer un document PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Récupérer les vols
    flights = Flight.objects.all()

    # Créer les données pour le tableau
    data = [['Image', 'Airline', 'Flight Name', 'Flight Number', 'Departure City', 'Arrival City', 'Departure Date', 'Arrival Date', 'Price Per Place']]
    
    for flight in flights:
        image_path = flight.image.path if flight.image else None
        image = Image(image_path, width=0.5 * inch, height=0.5 * inch) if image_path else "No Image"
        
        # Ajouter une ligne pour chaque vol
        data.append([
            image,
            flight.airline,
            flight.flight_name,
            flight.flight_number,
            flight.departure_city,
            flight.arrival_city,
            flight.departure_date.strftime('%Y-%m-%d'),  # Formater la date
            flight.arrival_date.strftime('%Y-%m-%d'),    # Formater la date
            f"{flight.price_per_place} DT"
        ])

    # Créer le tableau avec des largeurs de colonnes
    column_widths = [0.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch]
    table = Table(data, colWidths=column_widths)

    # Appliquer un style au tableau
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

    # Ajouter un titre
    styles = getSampleStyleSheet()
    title = Paragraph("List of Flights", styles['Title'])

    # Construire le PDF
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
def flight_list(request):
    # Récupérer tous les vols
    flights = Flight.objects.all()

    # Fonctionnalité de recherche
    search_query = request.GET.get('q', '')
    if search_query:
        flights = flights.filter(
            Q(flight_name__icontains=search_query) |
            Q(flight_number__icontains=search_query) |
            Q(departure_city__icontains=search_query) |
            Q(arrival_city__icontains=search_query)
        )

    # Fonctionnalité de tri
    sort_by = request.GET.get('sort')  # Tri par défaut
    valid_sort_fields = [
  'departure_date', 'arrival_date', 'flight_number', 'price_per_place'  # Utilisation de price_per_place

    ]

    if sort_by in valid_sort_fields:
        flights = flights.order_by(sort_by)
    else:
        flights = flights.order_by('departure_date')  # Valeur par défaut

    # Pagination
    paginator = Paginator(flights, 3)  # 3 vols par page
    page_number = request.GET.get('page')  # Récupérer le numéro de la page de la requête
    try:
        flights_page = paginator.page(page_number)  # Récupérer la page demandée
    except PageNotAnInteger:
        flights_page = paginator.page(1)  # Si la page n'est pas un entier, renvoyer la première page
    except EmptyPage:
        flights_page = paginator.page(paginator.num_pages)  # Si la page est vide, renvoyer la dernière page

 # Obtenir des recommandations de vols
    user_id = request.user.id if request.user.is_authenticated else None
    recommendations = get_flight_recommendations(user_id) if user_id else []


    # Créer le contexte pour le rendu
    context = {
        'flights': flights_page,  # Utiliser la page paginée des vols
        'sort_by': sort_by,
        'search_query': search_query,  # Inclure la requête de recherche dans le contexte
        'page_obj': flights_page,  # Ajouter page_obj pour le template
        'is_paginated': paginator.num_pages > 1,  # Pour vérifier si la pagination est nécessaire
            'recommendations': recommendations,  # Ajoutez cette ligne

    }

    # Rendre la vue avec les vols trouvés
    return render(request, 'BackOffice/Flights/index.html', context)



# Initialisez le client Amadeus avec votre clé API et votre secret
# amadeus = Client(
#     client_id='sPkddZjO4G8ykoMcAY7zEc5lHoMXkWV1',
#     client_secret='tWlWSlxQ80IcDP8Q'  # Votre secret API
# )

# def search_flights(request):
#     if request.method == 'GET':
#         origin = request.GET.get('origin', 'LHR')  # Code de l'aéroport d'origine
#         destination = request.GET.get('destination', 'CDG')  # Code de l'aéroport de destination
#         departure_date = request.GET.get('departure_date', '2024-07-25')  # Date de départ
#         adults = request.GET.get('adults', 1)  # Nombre d'adultes

#         try:
#             # Assurez-vous que vous utilisez correctement la méthode `get` sur l'objet `amadeus.shopping.flight_offers`
#             response = amadeus.shopping.flight_offers.get(
#                 originLocationCode=origin,
#                 destinationLocationCode=destination,
#                 departureDate=departure_date,
#                 adults=adults
#             )

#             # Vérifiez si la réponse est valide
#             if response and hasattr(response, 'data'):
#                 flights = response.data  # Récupération des données des vols
#                 print(flights)  # Imprimez les vols pour déboguer

#         except ResponseError as error:
#             print(f"Erreur lors de la recherche de vols : {error}")

#         return render(request, 'search_flights.html')  # Rendre un template si ce n'est pas une requête GET

# def flight_list_front(request):
#     # Récupération des paramètres de la requête
#     origin = request.GET.get('origin', 'LHR')
#     destination = request.GET.get('destination', 'CDG')
#     departure_date = request.GET.get('departure_date', '2024-07-25')
#     adults = request.GET.get('adults', 1)

#     flights = []
#     popular_flights = []  # Remplacez ceci par votre logique pour obtenir des vols populaires

#     try:
#         # Requête pour rechercher des offres de vol
#         response = amadeus.shopping.flight_offers.get(
#             originLocationCode=origin,
#             destinationLocationCode=destination,
#             departureDate=departure_date,
#             adults=adults
#         )
        
#         # Vérifiez la structure de la réponse
#         if response and hasattr(response, 'data'):
#             flights = response.data  # Récupération des données des vols
#             print(flights)  # Imprimez les vols pour déboguer

#     except ResponseError as error:
#         print(f"Erreur lors de la recherche de vols : {error}")

#     context = {
#         'flights': flights,
#         'popular_flights': popular_flights,
#     }

#     return render(request, 'FrontOffice/Flights/index.html', context)
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
