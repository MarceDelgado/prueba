from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('buscar/', views.buscar_animales, name='buscar_animales'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name ='logout'),   # <-- Agregado logout
    path('registro/', views.registro, name='registro'),
	path('dashboard/', views.dashboard, name='dashboard'),
    
]