from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SolicitudAdopcion
from apps.core.models import Mascotas, Persona, Raza, Especie, Domicilio, Novedad, ObservacionesSeguimiento,VacunasSeguimiento,ContactMessage

# Formulario de registro de usuario
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    fecha_nacimiento = forms.DateField(
        required=True,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
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
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }

# Formulario Personas
# forms.py
class PersonasForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(persona__isnull=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'email', 'telefono', 'dni', 'fecha_nacimiento', 'domicilio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellido': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'dni': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'domicilio': forms.TextInput(attrs={'class':'form-control'})       }

# Formulario Mascotas
class MascotasForm(forms.ModelForm):
    class Meta:
        model = Mascotas
        fields = ["raza","sexo","tamanio","fecha_nac","observaciones", "fotos"]
        widgets = {
            'raza': forms.Select(attrs={'class':'form-select'}),
            'sexo': forms.Select(attrs={'class':'form-select'}),
            'tamanio': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nac': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'fotos': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

# Formulario Especie
class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }

# Formulario Raza
class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = ["especie", "nombre"]
        widgets = {
            'especie': forms.Select(attrs={'class':'form-select'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }

# Formulario Perfil del Usuario
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
#formulario de contacto
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model=ContactMessage
        fields=['nombre','telefono','email','mensaje']
        widgets={
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mensaje':forms.Textarea(attrs={'class':'form-control','rows':6}),
        }

# Formulario Domicilio
class DomicilioForm(forms.ModelForm):
    class Meta:
        model= Domicilio
        fields=['calle', 'numero', 'localidad','codigo_postal']
        widgets = {
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.Select(attrs={'class':'form-select'}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
        }

class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ['mensaje', 'telefono', 'direccion']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Contanos por qué querés adoptar a esta mascota...'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de contacto'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección (ciudad, barrio)'}),
        }
        labels = {
            'mensaje': 'Motivo / Información adicional',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ["titulo", "descripcion_corta", "contenido", "imagen"]
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion_corta': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'contenido': forms.Textarea(attrs={'class':'form-control','rows':6}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class EstadoInicialForm(forms.ModelForm):
    class Meta:
        model= Mascotas
        fields=["estado_inicial"]
        widgets ={
            'estado_inicial': forms.Textarea(attrs={'class':'form-control', 'rows':6}),
        }

class ObservacionesForm(forms.ModelForm):
    class Meta:
        model=ObservacionesSeguimiento
        fields=["titulo","detalle"]
        widgets={
            'titulo':forms.TextInput(attrs={'class':'form-control'}),
            'detalle': forms.Textarea(attrs={'class':'form-control','rows':6}),
        }

class VacunasForm(forms.ModelForm):
    class Meta:
        model=VacunasSeguimiento
        fields=["nombre_vacuna","proxima_dosis"]
        widgets={
            'nombre_vacuna': forms.TextInput(attrs={'class':'form-control'}),
            'proxima_dosis': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }