from django.contrib import admin 
from .models import  Raza, Especie, Mascotas

admin.site.register(Mascotas)
admin.site.register(Raza)
admin.site.register(Especie)

# Register your models here.
