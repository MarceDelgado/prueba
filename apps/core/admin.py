from django.contrib import admin 
from .models import  Raza, Especie, Mascotas,UserProfile

admin.site.register(Mascotas)
admin.site.register(Raza)
admin.site.register(Especie)
admin.site.register(UserProfile)

# Register your models here.
