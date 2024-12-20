from django.urls import path , include
from . import views

app_name = 'back'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('billing/', views.billing, name='billing'),
    path('pricing/', views.pricing, name='pricing'),
    path('404/', views.error_404, name='404error'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgetpassword/', views.forget_password, name='forgetpassword'),
    path('docs/', views.docs, name='docs'),
    path('faq/', views.faq, name='faq'),
    path('user/' , include('Person.urls')) , 



# docs
    path('accordions/', views.accordions, name='accordions'),
    path('alerts/', views.alerts, name='alerts'),
    path('badge/', views.badge, name='badge'),
    path('borders/', views.borders, name='borders'),
    path('breadcrumb/', views.breadcrumb, name='breadcrumb'),
    path('button-group/', views.button_group, name='button_group'),
    path('buttons/', views.buttons, name='buttons'),
    path('card/', views.card, name='card'),
    path('carousel/', views.carousel, name='carousel'),
    path('changelog/', views.changelog, name='changelog'),
    path('close-button/', views.close_button, name='close_button'),
    path('collapse/', views.collapse, name='collapse'),
    path('colored-links/', views.colored_links, name='colored_links'),
    path('colors/', views.colors, name='colors'),
    path('credits/', views.credits, name='credits'),
    path('dropdowns/', views.dropdowns, name='dropdowns'),
    path('forms/', views.forms, name='forms'),
    path('gulp/', views.gulp, name='gulp'),
    path('list-group/', views.list_group, name='list_group'),
    path('modal/', views.modal, name='modal'),
    path('navbar/', views.navbar, name='navbar'),
    path('navs-tabs/', views.navs_tabs, name='navs_tabs'),
    path('offcanvas/', views.offcanvas, name='offcanvas'),
    path('opacity/', views.opacity, name='opacity'),
    path('pagination/', views.pagination, name='pagination'),
    path('placeholders/', views.placeholders, name='placeholders'),
    path('popovers/', views.popovers, name='popovers'),
    path('progress/', views.progress, name='progress'),
    path('ratio/', views.ratio, name='ratio'),
    path('scrollspy/', views.scrollspy, name='scrollspy'),
    path('shadows/', views.shadows, name='shadows'),
    path('spinners/', views.spinners, name='spinners'),
    path('stacks/', views.stacks, name='stacks'),
    path('tables/', views.tables, name='tables'),
    path('text-truncation/', views.text_truncation, name='text_truncation'),
    path('text/', views.text, name='text'),
    path('toasts/', views.toasts, name='toasts'),
    path('tooltips/', views.tooltips, name='tooltips'),
    path('typography/', views.typography, name='typography'),
    path('vertical-rule/', views.vertical_rule, name='vertical_rule'),


]
