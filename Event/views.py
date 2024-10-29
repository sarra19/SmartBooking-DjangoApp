from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from .models import Event
import openai
from django.conf import settings
import os
import requests
from django.core.files.base import ContentFile
from io import BytesIO
import genai
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
from PIL import Image
import io


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)







def ai_generate_description(title):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate a detailed description for an event with the title in 4 lines: {title}"
    
    response = model.generate_content(prompt)
    return response.text




@csrf_exempt  # Use only for testing; set up CSRF tokens in production
def generate_description(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '')

            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            description = ai_generate_description(title)  # Use AI to generate description
            return JsonResponse({'description': description}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
        


def event_list(request):
    events = Event.objects.all()
    search_query = request.GET.get('q', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    sort_by = request.GET.get('sort')
    valid_sort_fields = ['start_date', 'end_date', 'price_per_place', 'number_places']
    if sort_by in valid_sort_fields:
        events = events.order_by(sort_by)
    else:
        events = events.order_by('start_date')  # Default sorting

    paginator = Paginator(events, 3)  # 3 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'BackOffice/Events/list.html', context)

def generate_image_from_description(description):
    try:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        print("Error generating image:", e)
        return None

def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        city = request.POST['city']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        price_per_place = request.POST['price_per_place']
        number_places = request.POST['number_places']

        # Manage event image
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
        else:
            uploaded_file_url = ''

        # Generate image if none is uploaded
        if not uploaded_file_url:
            image_url = generate_image_from_description(description)
            if image_url:
                image_response = requests.get(image_url)
                image = ContentFile(image_response.content, name=f"{title}_generated_image.png")
                uploaded_file_url = fs.save(image.name, image)  # Save the generated image

        # Create the event
        event = Event(
            title=title,
            description=description,
            location=location,
            city=city,
            start_date=start_date,
            end_date=end_date,
            price_per_place=price_per_place,
            number_places=number_places,
            image=uploaded_file_url
        )
        event.save()
        return redirect('Event:event_list')

    return render(request, 'BackOffice/Events/add.html')

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.location = request.POST['location']
        event.city = request.POST['city']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        event.price_per_place = request.POST['price_per_place']
        event.number_places = request.POST['number_places']

        # Manage updated image
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            event.image = fs.url(filename)

        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect('Event:event_list')

    context = {
        'event': event
    }
    return render(request, 'BackOffice/Events/edit.html', context)

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('Event:event_list')

def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="events.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(220, height - 50, "List of Events")
    p.setFont("Helvetica", 10)

    # Column headers
    p.setFont("Helvetica-Bold", 12)
    headers = ["Title", "City", "Location", "Start Date", "End Date"]
    x_positions = [80, 200, 300, 400, 500]
    y = height - 80

    for i, header in enumerate(headers):
        p.drawString(x_positions[i], y, header)
    y -= 20
    p.line(70, y + 10, width - 70, y + 10)

    # Fetch events data and draw each row
    events = Event.objects.all()
    row_alternate = [colors.whitesmoke, colors.lightgrey]  # Alternate row colors
    row_color_index = 0

    for event in events:
        p.setFillColor(row_alternate[row_color_index % 2])
        p.rect(70, y - 5, width - 140, 20, stroke=0, fill=1)

        p.setFillColor(colors.black)  # Reset text color
        p.setFont("Helvetica", 10)

        # Draw event details
        row_data = [
            event.title,
            event.city,
            event.location,
            event.start_date.strftime('%Y-%m-%d'),
            event.end_date.strftime('%Y-%m-%d')
        ]
        for i, data in enumerate(row_data):
            p.drawString(x_positions[i], y, str(data))

        y -= 25
        row_color_index += 1

        # New page if needed
        if y < 50:
            p.showPage()
            p.setFont("Helvetica-Bold", 16)
            p.drawString(220, height - 50, "List of Events")
            p.setFont("Helvetica-Bold", 12)
            y = height - 80
            for i, header in enumerate(headers):
                p.drawString(x_positions[i], y, header)
            y -= 20
            p.line(70, y + 10, width - 70, y + 10)

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(270, 10, "Generated by SmartBooking")
    p.drawString(width - 100, 10, f"Page {p.getPageNumber()}")

    p.showPage()
    p.save()
    return response

def event_list_front(request):
    events = Event.objects.all()
    
    search_query = request.GET.get('q', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    paginator = Paginator(events, 3)  # 3 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'FrontOffice/Events/listFront.html', context)

def detail_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event
    }
    return render(request, 'FrontOffice/Events/detail.html', context)