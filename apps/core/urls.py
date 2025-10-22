from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, buscar_animales,contacto, login_view, logout_view, registro, dashboard, eliminar_raza, crear_raza, eliminar_persona,
                    ListarMascotas, CrearMascota, ModificarMascota, EliminarMascota, ModificarEspecieView, CrearPersonaView)
from apps.core.views import ListarEspeciesView, crear_persona

urlpatterns = [
	path('', home, name='home'),
	path('buscar/', buscar_animales, name='buscar_animales'),
    path('contacto/', contacto, name='contacto'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view, name ='logout'),
    path('registro/', registro, name='registro'),
	path('dashboard/', dashboard, name='dashboard'),
    #url del abm mascotas
    path('lista/', ListarMascotas.as_view(), name='listar_mascotas'),
    path('crear/', CrearMascota.as_view(), name='crear_mascotas'),
	path('personas/crear/', CrearPersonaView.as_view(), name='crear_persona'),
    path('modificar/<int:pk>/', ModificarMascota.as_view(), name='modificar_mascotas'),
    path('eliminar/<int:pk>/', EliminarMascota.as_view(), name='eliminar_mascotas'),
    path('eliminar_raza/<int:raza_id>/', auth_views.eliminar_raza, name='eliminar_raza'),
    path('razas/', crear_raza, name = 'crear_raza'),
    path('personas/crear/', crear_persona, name='crear_persona'),
    path('persona/eliminar/<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
	path('especies/', ListarEspeciesView.as_view(), name='listar_especies'),
    path('especie/modificar/<int:pk>/', ModificarEspecieView.as_view(), name='modificar_especie'),
]