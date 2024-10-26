from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Event
from django.db.models import Q  # Import Q for querying
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import necessary classes
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def event_list(request):
    # Retrieve all events
    events = Event.objects.all()

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    # Sort functionality
    sort_by = request.GET.get('sort')  # Default sort
    valid_sort_fields = [
        'start_date', 'end_date', 'price_per_place', 'number_places'
    ]

    if sort_by in valid_sort_fields:
        events = events.order_by(sort_by)
    else:
        events = events.order_by('start_date')  # Default value

    # Pagination
    paginator = Paginator(events, 3)  # 3 events per page
    page_number = request.GET.get('page')  # Get the requested page number
    try:
        events_page = paginator.page(page_number)  # Retrieve the requested page
    except PageNotAnInteger:
        events_page = paginator.page(1)  # If page is not an integer, return the first page
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)  # If page is empty, return the last page

    # Create context for rendering
    context = {
        'events': events_page,  # Use the paginated events
        'search_query': search_query,  # Include search query in context
        'sort_by': sort_by,
        'is_paginated': paginator.num_pages > 1,  # Check if pagination is necessary
    }

    return render(request, 'BackOffice/Events/list.html', context)

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

        # Create the event with collected data
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

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Event

def download_pdf(request):
    # Create a HTTP response with PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="events.pdf"'

    # Create a canvas to draw on
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw the title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "List of Events")
    p.setFont("Helvetica", 10)

    # Draw column headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 80, "Title")
    p.drawString(300, height - 80, "City")
    
    # Draw a line under the headers
    p.line(90, height - 85, width - 90, height - 85)

    # Fetch events data
    events = Event.objects.all()

    # Draw the events data
    y = height - 100
    for event in events:
        p.setFont("Helvetica", 10)
        p.drawString(100, y, event.title)
        p.drawString(300, y, event.city)

        y -= 20  # Move down for the next event

        # Check if we need a new page
        if y < 80:
            p.showPage()
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, height - 50, "List of Events")
            p.setFont("Helvetica", 10)

            # Redraw column headers
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, height - 80, "Title")
            p.drawString(300, height - 80, "City")
            p.line(90, height - 85, width - 90, height - 85)
            y = height - 100

    # Draw footer with page number
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(270, 10, "Generated by SmartBooking")
    p.drawString(width - 100, 10, f"Page {p.getPageNumber()}")

    # Finalize the PDF
    p.showPage()
    p.save()
    return response
