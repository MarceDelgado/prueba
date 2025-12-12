from django.urls import path
from django.contrib.auth import views as auth_views
from . import views   # ← NECESARIO
from .views import (
    edit_profile, home, buscar_animales, contacto, login_view, logout_view, registro, dashboard, quienesSomos, lista_novedades,
    ListarMascotas, ListarMascotasUsuario, ListarNovedadesUsuario, crear_mascota, modificar_mascota, eliminar_mascota_ajax,
    ModificarEspecieView, EliminarEspecie, ListarEspeciesView, CrearEspecieView,
    crear_raza, listar_razas, eliminar_raza, modificar_raza, recuperar_contraseña, cambiar_password,
    listar_personas, crear_persona, eliminar_persona, modificar_persona, habilitar_persona,
    cambiar_contraseña_voluntariamente, filtrar_mascotas, explorar_especies,
    explorar_razas, mis_adopciones, detalle_mascota, crear_novedades, eliminar_novedades, listar_novedades, modificar_novedades,
    detalle_novedad, view_profile, seguimiento_adopciones,lista_mascotas_adoptadas,
    crear_observacion,modificar_observacion,eliminar_observacion,crear_vacuna,modificar_vacuna,eliminar_vacuna,crear_estado_mascota,modificar_estado_mascota
)

urlpatterns = [
    path('', home, name='home'),
    path('buscar/', buscar_animales, name='buscar_animales'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro, name='registro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('quienesSomos/', quienesSomos, name='quienes_somos'),

    # PERFIL
    path('perfil/', view_profile, name='view_profile'),
    path('perfil/editar/', edit_profile, name='edit_profile'),


    # ABM Mascotas
    path('filtrar_mascotas/', ListarMascotas.as_view(), name='listar_mascotas'),
    path('listar_mascotas_usuario/', ListarMascotasUsuario.as_view(), name='listar_mascotas_usuario'),
    path('crear_mascota/', crear_mascota, name='crear_mascotas'),
    path('modificar_mascota/<int:mascota_id>/', modificar_mascota, name='modificar_mascota'),
    path('eliminar_mascota_ajax/', eliminar_mascota_ajax, name='eliminar_mascotas'),

    # ABM Raza
    path('eliminar_raza/<int:raza_id>/', eliminar_raza, name='eliminar_raza'),
    path('crear_raza/', crear_raza, name='crear_raza'),
    path('listar_razas/', listar_razas, name='listar_razas'),
    path('modificar_raza/<int:raza_id>/', modificar_raza, name='modificar_raza'),

    # ABM Especie
    path('listar_especies/', ListarEspeciesView.as_view(), name='listar_especies'),
    path('eliminar_especie/<int:pk>/', EliminarEspecie.as_view(), name='eliminar_especie'),
    path('modificar_especie/<int:pk>/', ModificarEspecieView.as_view(), name='modificar_especie'),
    path('crear_especie/', CrearEspecieView.as_view(), name='crear_especie'),

    # ABM Persona
    path('listar_personas/', listar_personas, name='listar_personas'),
    path('modificar_persona/<int:id>/', modificar_persona, name='modificar_persona'),
    path('crear_persona/', crear_persona, name='crear_persona'),
    path('personas/<int:persona_id>/baja/', views.baja_persona_confirmar, name='baja_persona_confirmar'),
    path('habilitar_persona/<int:persona_id>/', habilitar_persona, name='habilitar_persona'),

    # ABM Novedades
    path('novedades/listar/', listar_novedades, name='listar_novedades'),
    path('listar_novedades_usuario/', ListarNovedadesUsuario.as_view(), name='listar_novedades_usuario'),
    path('novedades/crear/', crear_novedades, name='crear_novedades'),
    path('novedades/modificar/<int:novedad_id>/', modificar_novedades, name='modificar_novedades'),
    path('novedades/eliminar/<int:novedad_id>/', eliminar_novedades, name='eliminar_novedades'),
    path('novedad/<int:id>/', detalle_novedad, name='detalle_novedad'),


    # Recuperación de contraseña
    path('solicitar-recuperacion/', recuperar_contraseña, name='solicitar_recuperacion'),
    path('cambiar-password/<int:id>/', cambiar_password, name='cambiar_password'),
    path('cambiar_contraseña/', cambiar_contraseña_voluntariamente, name='cambiar_contraseña_voluntariamente'),

    # Filtro Mascotas
    path('filtrar_mascotas/', ListarMascotas.as_view(), name='filtrar_mascotas'),

    # Exploración
    path('explorar_especies/', explorar_especies, name='explorar_especies'),
    path('explorar_razas/<int:raza_id>/', explorar_razas, name='explorar_razas'),

    # Adopciones
    path('mis_adopciones/', mis_adopciones, name='mis_adopciones'),

    # Detalle mascota
    path("mascota/<int:mascota_id>/", views.detalle_mascota, name="detalle_mascota"),

    #Formulario de adopcion
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),

    #Formulario para enviar emails a los administradores
    path('contacto/enviar/', views.contacto_submit, name='contacto_submit'),

    #urls para el seguimiento de las mascotas adoptadas
    path('lista_mascotas_adoptadas/',lista_mascotas_adoptadas,name='lista_mascotas_adoptadas'),
    path('seguimiento_adopciones/<int:id>', seguimiento_adopciones, name='seguimiento_adopciones'),
    path('crear_observacion/<int:id>/', crear_observacion, name='crear_observacion'),
    path('modificar_observacion/<int:id>/', modificar_observacion, name='modificar_observacion'),
    path('eliminar_observacion/<int:id>/', eliminar_observacion, name='eliminar_observacion'),
    path('crear_vacuna/<int:id>/', crear_vacuna, name='crear_vacuna'),
    path('modificar_vacuna/<int:id>/', modificar_vacuna, name='modificar_vacuna'),
    path('eliminar_vacuna/<int:id>/', eliminar_vacuna, name='eliminar_vacuna'),
    path('crear_estado_mascota/<int:id>/', crear_estado_mascota, name='crear_estado_mascota'),
    path('modificar_estado_mascota/<int:id>/', modificar_estado_mascota, name='modificar_estado_mascota'),
    
]

 