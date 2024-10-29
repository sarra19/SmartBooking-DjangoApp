from django.urls import path
from . import views

app_name = 'Flight'  # Cela fait référence au namespace que tu utilises pour le back-office

urlpatterns = [
    path('list/', views.flight_list, name='flight_list'),
    path('create/', views.flight_create, name='flight_create'),
    path('<int:flight_id>/update/', views.flight_update, name='flight_update'),
    path('<int:flight_id>/delete/', views.flight_delete, name='flight_delete'),  # Supprimer un vol
        path('flights/', views.flight_list_front, name='flight_list_front'),
    path('flights/download_pdf/', views.download_flights_pdf, name='download_flights_pdf'),


]