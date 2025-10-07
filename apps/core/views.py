
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.core.models import Mascotas
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login, logout as auth_logout #importamos la funcion "authenticate"

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