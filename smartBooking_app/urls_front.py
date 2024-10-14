from django.urls import path
from . import views 

app_name = 'front'

urlpatterns = [
    
    path('' , views.indexF , name='indexF'),
    path('tour/' , views.tour , name='tour'),
    path('testimonial/' , views.testimonial , name='testimonial'),
    path('services/' , views.services , name='services'),
    path('packages/' , views.packages , name='packages'),
    path('guides/' , views.guides , name='guides'),
    path('gallery/' , views.gallery , name='gallery'),
    path('destination/' , views.destination , name='destination'),
    path('contact/' , views.contact , name='contact'),
    path('booking/' , views.booking , name='booking'),
    path('blog/' , views.blog , name='blog'),
    path('base/' , views.base , name='base'),
    path('about/' , views.about , name='about'),
    path('404/' , views.p404 , name='404'),
    
    

]