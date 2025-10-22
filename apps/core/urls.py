
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, buscar_animales,contacto, login_view, logout_view, registro, dashboard,
                    ListarMascotas, CrearMascota, ModificarMascota, EliminarMascota)

urlpatterns = [
	path('', home, name='home'),
	path('buscar/', buscar_animales, name='buscar_animales'),
    path('contacto/', contacto, name='contacto'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view, name ='logout'),   # <-- Agregado logout
    path('registro/', registro, name='registro'),
	path('dashboard/', dashboard, name='dashboard'),
    #url del abm mascotas
    path('lista/', ListarMascotas.as_view(), name='listar_mascotas'),
    path('crear/', CrearMascota.as_view(), name='crear_mascotas'),
    path('modificar/<int:pk>/', ModificarMascota.as_view(), name='modificar_mascotas'),
    path('eliminar/<int:pk>/', EliminarMascota.as_view(), name='eliminar_mascotas'),
    path('eliminar_raza/<int:raza_id>/', auth_views.eliminar_raza, name='eliminar_raza'),
    
]