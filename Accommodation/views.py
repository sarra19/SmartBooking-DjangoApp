from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Accommodation
from .forms import AccommodationForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.urls import reverse  # Import reverse here

# views.py

from django.http import JsonResponse
from transformers import pipeline  # Hugging Face's transformers library

# Initialize sentiment analysis model (only once, as it's costly)
sentiment_analyzer = pipeline("sentiment-analysis")
# Exemple de fonction sentiment_analyzer
def feedback_result(request):
    sentiment_label = request.GET.get("label", "neutral")
    score = request.GET.get("score", "0")
    emoji = request.GET.get("emoji", "🤔")

    context = {
        "sentiment_label": sentiment_label,
        "score": score,
        "emoji": emoji,
    }
    return render(request, "frontOffice/pages/Accommodation/feedback_result.html", context)

def sentiment_analyzer(feedback):
    # Ceci est juste un exemple. Assurez-vous que votre analyse renvoie des labels valides.
    if "happy" in feedback or "good" in feedback:
        return [{"label": "positive", "score": 1.00}]
    elif "sad" in feedback or "bad" in feedback:
        return [{"label": "negative", "score": 1.00}]
    else:
        return [{"label": "neutral", "score": 0.50}]
def sentiment_analysis(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback", "")
        accommodation_id = request.POST.get("accommodation_id")

        if feedback and accommodation_id:
            # Analyser le feedback
            result = sentiment_analyzer(feedback)
            sentiment = result[0]["label"]
            score = result[0]["score"]

            # Ajouter le feedback et le sentiment à l'hébergement correspondant
            accommodation = get_object_or_404(Accommodation, id=accommodation_id)
            accommodation.add_feedback(feedback, sentiment, score)

            # Définir l'emoji correspondant au sentiment
            emoji_map = {
                "positive": "😊",
                "negative": "😞",
                "neutral": "😐",
            }
            emoji = emoji_map.get(sentiment, "🤔")
            url = f"{reverse('accommodation:feedback_result')}?label={sentiment}&score={score}&emoji={emoji}"
            return redirect(url)

            # return JsonResponse({
            #     "label": sentiment,
            #     "score": score,
            #     "emoji": emoji,
            # })

    return JsonResponse({"error": "Invalid request"}, status=400)
# views.py


    
class ReviewDetailView(DetailView):
    model = Accommodation
    template_name = "frontOffice/pages/Accommodation/review_feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accommodation = self.object
        context['feedbacks'] = accommodation.feedbacks
        context['stats'] = accommodation.feedback_statistics()  # Include statistics
        
        # Debugging statements
        print("Feedbacks:", context['feedbacks'])  # Print feedbacks to the console
        print("Statistics:", context['stats'])      # Print statistics to the console
        
        return context
class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'frontOffice/pages/Accommodation/detail.html'
    context_object_name = 'accommodation'

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Accommodation, id=id)

# Liste des hébergements
class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'backOffice/pages/Accommodation/index.html'
    context_object_name = 'accommodations'
    paginate_by = 6

    def get_queryset(self):
        queryset = Accommodation.objects.all()

        # Fonctionnalité de recherche
        search_query = self.request.GET.get('search_query', '')
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            ) | queryset.filter(
                location__icontains=search_query
            )  | queryset.filter(
                description__icontains=search_query
            )

        # Tri
        sort_field = self.request.GET.get('sort', 'name')
        valid_sort_fields = ['name', 'price_per_night', 'rating', 'type_of_accommodation']
        if sort_field in valid_sort_fields:
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('name')

        return queryset.order_by(sort_field) if sort_field in valid_sort_fields else queryset.order_by('name')

# Détails d'un hébergement
class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'backOffice/pages/Accommodation/details.html'
    context_object_name = 'accommodation'



def add_accommodation(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        description = request.POST['description']
        type_of_accommodation = request.POST['type_of_accommodation']
        price_per_night = request.POST['price_per_night']
        amenities = request.POST.getlist('amenities')  # Assuming amenities are selected as checkboxes

        # Manage accommodation image upload
        uploaded_file_url = ''
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)

        # Create the accommodation entry with collected data
        accommodation = Accommodation(
            name=name,
            location=location,
            description=description,
            type_of_accommodation=type_of_accommodation,
            price_per_night=price_per_night,
            amenities=", ".join(amenities),  # Store amenities as comma-separated string
            image=uploaded_file_url  # Set the image URL if uploaded
        )
        accommodation.save()  # Save the accommodation instance

        messages.success(request, "Hébergement ajouté avec succès !")  # Show success message
        return redirect('accommodation:accommodation_list')

    return render(request, 'backOffice/pages/Accommodation/add.html')


# Mettre à jour un hébergement
# class AccommodationUpdateView(UpdateView):
#     model = Accommodation
#     form_class = AccommodationForm
#     template_name = 'backOffice/pages/Accommodation/update.html'
#     success_url = reverse_lazy('accommodation:accommodation_list')

#     def form_valid(self, form):
#         messages.success(self.request, "Hébergement mis à jour avec succès !")
#         return super().form_valid(form)

def edit_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    
    if request.method == 'POST':
        accommodation.name = request.POST['name']
        accommodation.description = request.POST['description']
        accommodation.location = request.POST['location']
        accommodation.type_of_accommodation = request.POST['type_of_accommodation']
        accommodation.price_per_night = request.POST['price_per_night']
        accommodation.amenities = request.POST.getlist('amenities')  # Use getlist for multiple amenities

        # Manage updated image
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            accommodation.image = fs.url(filename)

        accommodation.save()
        messages.success(request, "Accommodation updated successfully!")
        return redirect('accommodation:accommodation_list')  # Update with the correct redirect URL

    context = {
        'accommodation': accommodation,
        'TYPE_OF_ACCOMMODATION_CHOICES': Accommodation.TYPE_OF_ACCOMMODATION_CHOICES,
        'AMENITIES_CHOICES': Accommodation.AMENITIES_CHOICES
    }
    return render(request, 'BackOffice/pages/Accommodation/update.html', context)

# Supprimer un hébergement
class AccommodationDeleteView(DeleteView):
    model = Accommodation
    template_name = 'backOffice/pages/Accommodation/delete.html'
    success_url = reverse_lazy('accommodation:accommodation_list')

    def get_success_url(self):
        messages.success(self.request, "Hébergement supprimé avec succès !")
        return super().get_success_url()
#FRONT

# views.py - List Accommodations (Front End)

class ListAccommodationsFront(ListView):
    model = Accommodation
    context_object_name = "accommodations"
    template_name = 'frontOffice/pages/Accommodation/index.html'
    paginate_by = 6

    def get_queryset(self):
        return Accommodation.objects.all().order_by('id')

    def post(self, request, *args, **kwargs):
        accommodation_id = request.POST.get('accommodation_id')
        accommodation = get_object_or_404(Accommodation, id=accommodation_id)

        rating = request.POST.get('rating')  # Récupérer la notation du formulaire
        if rating:
            accommodation.update_rating(float(rating))  # Met à jour la notation de l'hébergement

        return redirect('accommodation:list_front')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def download_pdf(request):
    # Create a HTTP response with PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="accommodations.pdf"'

    # Create a canvas to draw on
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw the title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "List of Accommodations")
    p.setFont("Helvetica", 10)

    # Draw column headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 80, "Name")
    p.drawString(300, height - 80, "Location")
    p.drawString(400, height - 80, "Type")
    p.drawString(500, height - 80, "Price per Night")

    # Draw a line under the headers
    p.line(90, height - 85, width - 90, height - 85)

    # Fetch accommodations data
    accommodations = Accommodation.objects.all()

    # Draw the accommodations data
    y = height - 100
    for accommodation in accommodations:
        p.setFont("Helvetica", 10)
        p.drawString(100, y, accommodation.name)
        p.drawString(300, y, accommodation.location)
        p.drawString(400, y, accommodation.type_of_accommodation)
        p.drawString(500, y, f"${accommodation.price_per_night:.2f}")

        y -= 20  # Move down for the next accommodation

        # Check if we need a new page
        if y < 80:
            p.showPage()
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, height - 50, "List of Accommodations")
            p.setFont("Helvetica", 10)

            # Redraw column headers
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, height - 80, "Name")
            p.drawString(300, height - 80, "Location")
            p.drawString(400, height - 80, "Type")
            p.drawString(500, height - 80, "Price per Night")
            p.line(90, height - 85, width - 90, height - 85)
            y = height - 100

    # Draw footer with page number
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(270, 10, "Generated by SmartBooking")
    # Note: p.getPageNumber() will not work directly; you can manually track the page number if needed.

    # Finalize the PDF
    p.showPage()
    p.save()
    return response