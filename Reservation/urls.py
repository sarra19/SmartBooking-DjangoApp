from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [

 #Reservation
    path('Rsv/', views.Rsv.as_view(), name='Rsv'),  # Use as_view() for class-based views
    path('add-reservation/', views.AddReservationView.as_view(), name='add_reservation'),  
    path('update-reservation/<int:pk>/', views.UpdateReservationView.as_view(), name='update_reservation'),  
    path('delete-reservation/<int:pk>/', views.delete_reservation.as_view(), name='delete_reservation'),  
    path('details_reservation/<int:pk>/', views.detailsReservation, name='details_reservation'), 

#front
     path('Rsv-flight-front/', views.RsvFlightFront.as_view(), name='Rsv-flight-front'),  # Use as_view() for class-based views
     path('Rsv-event-front/', views.RsvEventFront.as_view(), name='Rsv-event-front'),  # Use as_view() for class-based views

     path('Rsv-flight-front/<int:pk>/Accomodation/', views.RsvAccfront.as_view(), name='Rsv-Acc-front'),  # Use as_view() for class-based views

     # path('Rsv-flight-front/<int:pk>/Accomodation/<int:ak>/Transport', views.RsvTrsfront.as_view(), name='Rsv-Trs-front'),  # Use as_view() for class-based views
     
     path('Rsv-flight-front/<int:pk>/Accomodation/<int:ak>/addReservation', views.AddRsvfront.as_view(), name='Rsv-front'),  # Use as_view() for class-based views
    
     path('my-reservations/<int:pk>/', views.my_reservations.as_view(), name='myreservation'),

     path('delete-freservation/<int:pk>/', views.delete_freservation.as_view(), name='delete-freservation'),  


#event
     path('RsvFrontEvent/<int:ek>/addReservation', views.AddRsvEventfront.as_view(), name='RsvFrontEvent'),  # Use as_view() for class-based views


path('accept/<int:id>/', views.accept_reservation, name='accept_reservation'),
    path('reject/<int:id>/', views.reject_reservation, name='reject_reservation'),
]