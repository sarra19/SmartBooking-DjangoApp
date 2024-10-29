"""
URL configuration for smartBooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from smartBooking_app.views import signin  # Assurez-vous d'importer la vue home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('front/' , include('smartBooking_app.urls_front', namespace='front')),
    path ('back/' , include('smartBooking_app.urls_back', namespace='back')),
    path('', signin, name='signin'),  # Ajoutez cette ligne pour rediriger vers la vue home
    path('flights/', include('Flight.urls', namespace='Flight')),  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)