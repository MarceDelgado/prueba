from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, buscar_animales,contacto, login_view, logout_view, registro, dashboard,
                    ListarMascotas,ListarMascotasUsuario, crear_mascota, ModificarMascota, eliminar_mascota,
                    ModificarEspecieView, EliminarEspecie,ListarEspeciesView,CrearEspecieView,
                    crear_raza,listar_razas,eliminar_raza,modificar_raza, recuperar_contraseña, cambiar_password,
                    listar_personas,crear_persona, eliminar_persona, modificar_persona,habilitar_persona,
                    cambiar_contraseña_voluntariamente, filtrar_mascotas, explorar_especies, explorar_razas, mis_adopciones)
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
    path('listar_mascotas_usuario/', ListarMascotasUsuario.as_view(), name='listar_mascotas_usuario'),
    path('crear_mascota/', crear_mascota, name='crear_mascotas'),
    path('modificar_mascota/<int:pk>/', ModificarMascota.as_view(), name='modificar_mascotas'),
    path('eliminar_mascota/<int:id>/', eliminar_mascota, name='eliminar_mascotas'),
    #url del abm raza
    path('eliminar_raza/<int:raza_id>/',eliminar_raza, name='eliminar_raza'),
    path('crear_raza/', crear_raza, name = 'crear_raza'),
    path('listar_razas/', listar_razas, name='listar_razas'),
    path('modificar_raza/<int:raza_id>', modificar_raza,name='modificar_raza'),
    #url del abm especie
    path('listar_especies/', ListarEspeciesView.as_view(), name='listar_especies'),
    path('eliminar_especie/<int:pk>/',EliminarEspecie.as_view(), name='eliminar_especie'),
    path('modificar_especie/<int:pk>/', ModificarEspecieView.as_view(), name='modificar_especie'),
    path('crear_especie/',CrearEspecieView.as_view(), name='crear_especie'),
    #url del abm persona(adoptante)
    path('listar_personas/', listar_personas,name='listar_personas'),
    path('modificar_persona/<int:id>/',modificar_persona, name='modificar_persona'),
    path('crear_persona/', crear_persona, name='crear_persona'),
    path('eliminar_persona/<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
    path('habilitar_persona/<int:persona_id>/', habilitar_persona, name='habilitar_persona'),
    #correo
    path('solicitar-recuperacion/', recuperar_contraseña, name='solicitar_recuperacion'),
    path('cambiar-password/<int:id>/', cambiar_password, name='cambiar_password'),
    path('cambiar_contraseña', cambiar_contraseña_voluntariamente, name='cambiar_contraseña_voluntariamente'),
    #FILTRO MASCOTAS (nuevo)
    path('filtrar_mascotas/', filtrar_mascotas, name='filtrar_mascotas'),
    path('explorar_especies/', explorar_especies, name='explorar_especies'),
    path('explorar_razas/<int:especie_id>/', explorar_razas, name='explorar_razas'),
    path('mis_adopciones/', mis_adopciones, name='mis_adopciones'),
]
 