from django.contrib import admin 
from .models import  Raza, Especie, Mascotas,UserProfile, Persona, SolicitudAdopcion, Novedad,ObservacionesSeguimiento,VacunasSeguimiento, ContactMessage

admin.site.register(Mascotas)
admin.site.register(Raza)
admin.site.register(Especie)
admin.site.register(UserProfile)
admin.site.register(Persona)
admin.site.register(ObservacionesSeguimiento)
admin.site.register(VacunasSeguimiento)
admin.site.register(ContactMessage)

# Register your models here.

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'usuario', 'fecha_solicitud', 'estado')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('usuario__username', 'usuario__email', 'mascota__nombre')
    readonly_fields = ('fecha_solicitud',)

