from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, buscar_animales,contacto, login_view, logout_view, registro, dashboard,
                    ListarMascotas, crear_mascota, ModificarMascota, eliminar_mascota,
                    ModificarEspecieView, EliminarEspecie,ListarEspeciesView,CrearEspecieView,
                    crear_raza,listar_razas,eliminar_raza,modificar_raza,
                    listar_personas,crear_persona, eliminar_persona, modificar_persona)

urlpatterns = [
	path('', home, name='home'),
	path('buscar/', buscar_animales, name='buscar_animales'),
    path('contacto/', contacto, name='contacto'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view, name ='logout'),
    path('registro/', registro, name='registro'),
	path('dashboard/', dashboard, name='dashboard'),
    #url del abm mascotas
    path('listar_mascotas/', ListarMascotas.as_view(), name='listar_mascotas'),
    path('crear_mascota/', crear_mascota, name='crear_mascotas'),
    path('modificar_mascota/<int:pk>/', ModificarMascota.as_view(), name='modificar_mascotas'),
    path('eliminar_mascota/<int:id>/', eliminar_mascota, name='eliminar_mascotas'),
    #url del abm raza
    path('eliminar_raza/<int:raza_id>/',eliminar_raza, name='eliminar_raza'),
    path('crear_raza/', crear_raza, name = 'crear_raza'),
    path('listar_razas/', listar_razas, name='listar_razas'),
    path('modificar_raza/<int:id>',modificar_raza,name='modificar_raza'),
    #url del abm especie
    path('listar_especies/', ListarEspeciesView.as_view(), name='listar_especies'),
    path('eliminar_especie/<int:pk>/',EliminarEspecie.as_view(), name='eliminar_especie'),
    path('modificar_especie/<int:pk>/', ModificarEspecieView.as_view(), name='modificar_especie'),
    path('crear_especie/',CrearEspecieView.as_view(), name='crear_especie'),
    #url del abm persona(adoptante)
    path('listar_personas/', listar_personas,name='listar_personas'),
    path('modificar_persona/<int:id>/',modificar_persona, name='modificar_persona'),
    path('crear_persona/', crear_persona, name='crear_persona'),
    path('eliminar_persona<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
]