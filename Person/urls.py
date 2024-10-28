from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('register/', register, name="register"),
    path('logout/', LogoutView.as_view() , name="logout"),
    path('login/', Login_user , name="login"),
    path('create/', PersonCreateView.as_view(), name='create_person'),
    path('list/', PersonListView.as_view(), name='list_persons'),
    path('update/<str:pk>/', PersonUpdateView.as_view(), name='update_person'),
    path('delete/<str:pk>/', PersonDeleteView.as_view(), name='delete_person'),
    path('settings/', settings_view, name='settings_view'),
    path('remove-avatar/', remove_avatar, name='remove_avatar'),
    path('settingsProfile/', settingsProfile, name='settingsProfile'),

] 
