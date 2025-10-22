from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from apps.core.models import Especie, Mascotas, Raza, Persona
from .forms import EspecieForm, RazaForm, RegistroUsuarioForm, MascotasForm, PersonaForm
from django.contrib.auth import authenticate, login, logout as auth_logout #importamos la funcion "authenticate"

from django.views.generic import CreateView, UpdateView, DeleteView, ListView #importamos las clases bases para el abm

def home(request):
    return render(request, 'home.html', {})

def buscar_animales(request):
    # Lógica para buscar animales (por ahora puede ser un render simple)
    return render(request, 'buscar_resultados.html')

def contacto(request):
    if request.method == 'POST':
        # Aquí podrías procesar el formulario
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        # Guardar datos o enviar mail...
        return render(request, 'contacto_exito.html')
    return render(request, 'contacto.html')


def login_view(request):   
   #FUNCION DE VISTA DEL LOGEO PARA INICIAR SESION
   user = None  # Inicializamos la variable user fuera del bloque condicional

   if request.method == 'POST':
       print('viene por POST')
       username = request.POST.get('username')  # para obtener el usuario
       password = request.POST.get('password')  # para obtener la contraseña
       print(username)
       print(password)

       user = authenticate(request, username=username, password=password)
       #print(user)  # Imprimimos lo siguiente para saber si está funcionando bien

       if user is not None:
          login(request, user)
          return redirect('dashboard')
       else:
        mensaje = 'usuario y/o contraseña incorrecta'
        contexto = {
            'mensaje': mensaje,
         }
        return render(request, 'login.html', contexto)

   #contexto = {}  # Esto está en un bloque que no se ejecutará
   return render(request, 'login.html')

def dashboard(request):
   lista_mascotas = Mascotas.objects.all()
   contexto = {
       'mascotas' : lista_mascotas
   }
   return render(request, 'dashboard.html', contexto)

def logout_view(request):
   auth_logout(request)
   return redirect('home')

def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada con éxito!")
            return redirect("login")
        else:
            messages.error(request, "Ocurrió un error. Verificá los datos.")
    else:
        form = RegistroUsuarioForm()
    
    return render(request, "registro.html", {"form": form})

#abm mascotas
#abm cbv
class ListarMascotas(ListView):
    model=Mascotas
    template_name='mascotas/listaMascotas.html'

class ModificarMascota(UpdateView):
    model=Mascotas
    form_class=MascotasForm
    template_name='mascotas/modificar.html'
    success_url=reverse_lazy('listar_mascotas')

class CrearMascota(CreateView):
    model=Mascotas
    form_class=MascotasForm
    template_name='mascotas/crear.html'
    success_url=reverse_lazy('listar_mascotas')
    
class EliminarMascota(DeleteView):
    model=Mascotas
    template_name='mascotas/eliminar.html'
    success_url=reverse_lazy('listar_mascotas')

#abm fbv
def crear_mascota(request):
    if request.method=='POST':
        raza=request.POST.get('raza')
        sexo=request.POST.get('sexo')
        tamanio=request.POST.get('tamanio')
        observaciones=request.POST.get('observaciones')
        fecha_nac=request.POST.get('fecha_nac')

        nueva_mascota=Mascotas(
            raza=raza,
            sexo=sexo,
            tamanio=tamanio,
            observaciones=observaciones,
            fecha_nac=fecha_nac
        )

        nueva_mascota.save()
        return redirect('listar_mascotas')
    
    return render(request, 'crear.html')

def eliminar_mascota(request):
    pass

#abm raza(fbv)
#crear->cami
def crear_raza(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')

        especie = None
        if especie:  # si el usuario seleccionó alguna especie
            especie = get_object_or_404(Especie, id=especie)

        nuevaRaza = Raza (
            nombre = nombre,
            especie = especie
        )
        
        nuevaRaza.save()
        return redirect('listar_razas')
    
    especies = Especie.objects.all()
    return render(request, 'crearRaza.html', {'especies': especies})

#eliminar->marce
def eliminar_raza(request, raza_id):
    #Obtiene la raza por su id, si no existe se genera error
    raza = get_object_or_404(Raza, id=raza_id)
    
    #Si el formulario se envia, se confirma la eliminacion
    if request.method == 'POST':
        try:
            #Elimina el objeto si lo encuentra 
            raza.delete()
   
        #Mensaje de exito
        messages.success(request, "La raza ha sido eliminada exitosamente.")
    
    #Redirige a la lista de razas
    return redirect('lista_razas')

#modificar-> jessi
def modificar_raza(request, raza_id):
    # Obtiene la instancia de la raza que se va a modificar
    raza = get_object_or_404(Raza, id=raza_id) # type: ignore
    
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('listar_razas')  # Redirige a la lista de razas después de la modificación
    else:
        form = RazaForm(instance=raza)  # Prellenamos el formulario con la instancia existente

    return render(request, 'modificar_raza.html', {'form': form})

#listar

#abm especie(cbv)
#crear->jessi
class CrearEspecieView(CreateView):
    model = Especie
    form_class = EspecieForm
    template_name = 'crearEspecie.html'
    success_url = reverse_lazy('listar_especies')  # Redirige a la lista de especies después de crear
    
#eliminar
#modificar->cami
class ModificarEspecieView(CreateView):
    model = Especie
    form_class = EspecieForm
    template_name = 'modificarEspecie.html'
    success_url = reverse_lazy('listar_especies')

#listar->marce

#abm personas(fbv)
#crear->marce
#modificar->yo
#eliminar->cami
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    persona.delete()
  
    return redirect('eliminarPersona')

#listar->jessi