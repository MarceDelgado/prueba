
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.core.models import Mascotas, Persona

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
#Formulario Personas
class PersonasForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'edad', 'email','telefono']       

#formulario para las mascotas
class MascotasForm(forms.ModelForm):
    class Meta:
        model=Mascotas
        fields=["raza","sexo","tamanio","fecha_nac","observaciones"]

#formulario Especie
class EspecieForm(forms.ModelForm):
    class Meta:
        model= Mascotas
        fields=["nombre"]

#formulario Raza
class RazaForm(forms.ModelForm):
    class Meta:
        model= Mascotas
        fields=["especie", "nombre"]

#HOLA ESTOY PROBNDO UE FUNCIONE EL GIT 
