from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import download_pdf  # Ensure you import the view

app_name = 'accommodation'
urlpatterns = [
    path('accommodation_list/',  views.AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodation_detail/<int:pk>/',  views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('add_accommodation/',  views.add_accommodation, name='add_accommodation'),
    path('accommodation_update/<int:accommodation_id>/',  views.edit_accommodation, name='accommodation_update'),
    path('accommodation_delete/<int:pk>/',  views.AccommodationDeleteView.as_view(), name='accommodation_delete'),
    path('download/', download_pdf, name='download_pdf'),  # Add this line
   

#front 

path('accommodation_list_front', views.ListAccommodationsFront.as_view(), name='accommodation_list_front'),
path("api/sentiment-analysis/", views.sentiment_analysis, name="sentiment_analysis"),
path('feedback_result/', views.feedback_result, name='feedback_result'),
path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),  # Corrected line
path('detail/<int:id>/', views.AccommodationDetailView.as_view(), name='detail'),



    # path('add/', views.AddAccommodationFront.as_view(), name='accommodation_add'),
#    # path('<int:pk>/delete/', views.DeleteAccommodationFront.as_view(), name='accommodation_delete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
