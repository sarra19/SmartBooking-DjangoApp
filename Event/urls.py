from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import download_pdf  # Ensure you import the view


app_name = 'Event'  # Cela doit être défini avant urlpatterns

urlpatterns = [
    path('list/', views.event_list, name='event_list'),
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit event URL
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete event URL
    path('events/download/', download_pdf, name='download_pdf'),  # Add this line

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)