from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import download_pdf  # Ensure you import the view
from .views import generate_description
from .views import generate_image


app_name = 'Event'  # Cela doit être défini avant urlpatterns

urlpatterns = [
    path('list/', views.event_list, name='event_list'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit event URL
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete event URL
    path('events/download/', download_pdf, name='download_pdf'),  # Add this line
    path('listFront/', views.event_list_front, name='event_list_front'),
    path('', views.event_list, name='event_list'),
    path('detail/<int:event_id>/', views.detail_event, name='detail_event'),
    path('generate-description/', generate_description, name='generate_description'),
    path('generateImage/' , generate_image , name="generate_image"),

]
