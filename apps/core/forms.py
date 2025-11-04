from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from apps.core.models import Mascotas, Persona,Raza,Especie, Domicilio

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    fecha_nacimiento = forms.DateField(
            required=True,
            label="Fecha de nacimiento",
            widget=forms.DateInput(attrs={'type': 'date'})
        )
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
    user=forms.ModelChoiceField(
        queryset=User.objects.filter(persona__isnull=True),
        required=False,
        label="Usuario asociado"
    )
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'email','telefono', 'dni', 'fecha_nacimiento', 'puede_adoptar', 'user']     

#formulario para las mascotas
class MascotasForm(forms.ModelForm):
    class Meta:
        model=Mascotas
        fields=["raza","sexo","tamanio","fecha_nac","observaciones", "fotos"]

#formulario Especie
class EspecieForm(forms.ModelForm):
    class Meta:
        model= Especie
        fields=["nombre"]

#formulario Raza
class RazaForm(forms.ModelForm):
    class Meta:
        model= Raza
        fields=["especie", "nombre"]

#formulario Perfil del Usuario
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

#formulario para domicilio
class DomicilioForm(forms.ModelForm):
    class Meta:
        model= Domicilio
        fields=['calle', 'numero', 'localidad','codigo_postal']

