from django.contrib import admin 
from .models import  Raza, Especie, Mascotas,UserProfile, Persona

admin.site.register(Mascotas)
admin.site.register(Raza)
admin.site.register(Especie)
admin.site.register(UserProfile)
admin.site.register(Persona)


# Register your models here.
