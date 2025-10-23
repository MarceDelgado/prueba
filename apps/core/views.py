from django.urls import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from apps.core.models import Especie, Mascotas, Raza,Persona
from .forms import EspecieForm, RazaForm, RegistroUsuarioForm, MascotasForm, PersonasForm
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

#ABM MASCOTAS(cbv,fbv) sabri
class ListarMascotas(ListView):
    model=Mascotas
    template_name='mascotas/listaMascotas.html'

class ModificarMascota(UpdateView):
    model=Mascotas
    form_class=MascotasForm
    template_name='mascotas/modificarMascota.html'
    success_url=reverse_lazy('listar_mascotas')

def crear_mascota(request):
    if request.method=='POST':
        form=MascotasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form=MascotasForm()
    return render(request, 'mascotas/crearMascota.html', {'form':form})

def eliminar_mascota(request, id):
    mascota=get_object_or_404(Mascotas, pk=id)
    if request.method=='POST':
        mascota.delete()
        return redirect('listar_mascotas')
    return render(request,'mascotas/eliminarMascota.html', {'mascota':mascota})

#ABM RAZA(fbv)
#listar-> sabri
def listar_razas(request):
    razas=Raza.objects.all()
    return render(request, 'raza/listarRaza.html',{'razas':razas})

#crear->cami
def crear_raza(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especie_id = request.POST.get('especie')

        especie = None
        if especie_id:  # si el usuario seleccionó alguna especie
            especie = get_object_or_404(Especie, id=especie_id)

        nuevaRaza = Raza (
            nombre = nombre,
            especie = especie
        )
        
        nuevaRaza.save()
        return redirect('listar_razas')
    
    especies = Especie.objects.all()
    return render(request, 'raza/crearRaza.html', {'especies': especies})

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
        except Exception as e:
            messages.error(request, f"Error al eliminar la raza: {e}")
         #Redirige a la lista de razas
        return redirect('listar_razas')
    #Si el metodo no es POST, muestra el formulario de confirmacion
    return render(request, 'raza/eliminarRaza.html', {'raza': raza})

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

    return render(request, 'raza/modificarRaza.html', {'form': form})


#ABM ESPECIE(cbv)
#crear->jessi
class CrearEspecieView(CreateView):
    model = Especie
    form_class = EspecieForm
    template_name = 'especie/crearEspecie.html'
    success_url = reverse_lazy('listar_especies')  # Redirige a la lista de especies después de crear
#eliminar->sabri
class EliminarEspecie(DeleteView):
    model=Especie
    template_name='especie/eliminarEspecie.html'
    success_url=reverse_lazy('listar_especies')

#modificar->cami
class ModificarEspecieView(UpdateView):
    model = Especie
    form_class = EspecieForm
    template_name = 'especie/modificarEspecie.html'
    success_url = reverse_lazy('listar_especies')

#listar->marce
class ListarEspeciesView(ListView):
    model = Especie
    #Nombre del archivo html
    template_name = 'especie/listarEspecie.html'
    #Nombre con el que se accede a las especies
    context_object_name = 'especies'
    

#ABM PERSONA(fbv)
#crear->marce
def crear_persona(request):
    if request.method == 'POST':
        #Si el formulario es valido se envia
        form = PersonasForm(request.POST)
        if form.is_valid():
            #se guarda el formulario
            form.save()
            #redirigimos a la lista de personas
            return redirect('listar_personas')
    else:
            #si es un GET, se muestra el formulario vacio
            form = PersonasForm()
    return render(request, 'personas/crearPersonas.html', {'form': form})
    

#modificar->sabri
def modificar_persona(request, id):
    persona=get_object_or_404(Persona,pk=id)
    if request.method=='POST':
        form=PersonasForm(request.POST, instance=persona)
        if form.is_valid():
            persona.save()
            return redirect('listar_personas')
    else:
        form=PersonasForm(instance=persona)
    return render(request,'personas/modificarPersona.html',{'form':form})

#eliminar->cami
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)

    if request.method == 'POST':
       persona.delete()
   
    return render(request, 'personas/eliminarPersona.html', {'persona': persona})

#listar->jessi
def listar_personas(request):
    persona = Persona.objects.all()
    return render(request, 'personas/listarPersonas.html', {'personas': persona})
