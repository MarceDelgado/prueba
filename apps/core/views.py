#el menuAdmin(dashboard), te paso la vista para que verifiques solo la parte de administrador
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.core.models import Especie, Mascotas, Raza, Persona, Adopcion
from .forms import EspecieForm, RazaForm, RegistroUsuarioForm, MascotasForm, PersonasForm, DomicilioForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout as auth_logout  # importamos la funcion "authenticate"
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View  # importamos las clases bases para el abm
from .models import Localidad, UserProfile

# correo
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .emails import enviar_correo
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.hashers import make_password
import random, string

# decoradores
from django.contrib.auth.decorators import login_required  # -> para fbv
from django.utils.decorators import method_decorator  # -> para cbv


# =======================
# PÁGINAS PÚBLICAS
# =======================
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


# =======================
# LOGIN / REGISTRO / PERFIL
# =======================
def login_view(request):
   # FUNCION DE VISTA DEL LOGEO PARA INICIAR SESION
   user = None  # Inicializamos la variable user fuera del bloque condicional

   if request.method == 'POST':
       print('viene por POST')
       username = request.POST.get('username')  # para obtener el usuario
       password = request.POST.get('password')  # para obtener la contraseña
       print(username)
       print(password)

       user = authenticate(request, username=username, password=password)

       if user is not None:
            login(request, user)
            if user.userprofile.primer_ingreso:
                return redirect('cambiar_password', id=user.userprofile.id)
            return redirect('dashboard')
       else:
            mensaje = 'usuario y/o contraseña incorrecta'
            contexto = {'mensaje': mensaje}
            return render(request, 'login.html', contexto)

   return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def logout_view(request):
   auth_logout(request)
   return redirect('home')


def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            fecha_nac = form.cleaned_data['fecha_nacimiento']
            # esto es para asociar el usuario a una persona
            Persona.objects.create(
                nombre=user.first_name,
                apellido=user.last_name,
                email=user.email,
                user=user,
                fecha_nacimiento=fecha_nac,
                puede_adoptar=False
            )
            messages.success(request, "¡Tu cuenta ha sido creada con éxito!")
            return redirect("login")
        else:
            messages.error(request, "Ocurrió un error. Verificá los datos.")
    else:
        form = RegistroUsuarioForm()
    
    return render(request, "registro.html", {"form": form})


# =======================
# ABM MASCOTAS (cbv, fbv) sabri
# =======================
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Restringir_acceso(View):  # para el decorador login_required de las clases
    pass


class ListarMascotas(Restringir_acceso, ListView):
    model = Mascotas
    template_name = 'admin/mascotas/listaMascotas.html'


class ListarMascotasUsuario(ListView):
    model = Mascotas
    template_name = 'user/listaMascotas.html'
    context_object_name = 'mascotas_list'

    def get_queryset(self):
        qs = super().get_queryset()
        raza_id=self.request.GET.get("raza")
        if raza_id:
            qs = qs.filter(raza_id=raza_id)
        return qs                                    
        


class ModificarMascota(UpdateView, Restringir_acceso):
    model = Mascotas
    form_class = MascotasForm
    template_name = 'admin/mascotas/modificarMascota.html'
    success_url = reverse_lazy('listar_mascotas')


@login_required(login_url='/login/')
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotasForm()
    return render(request, 'admin/mascotas/crearMascota.html', {'form': form})


@login_required(login_url='/login/')
def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascotas, pk=id)
    if request.method == 'POST':
        mascota.delete()
        return redirect('listar_mascotas')
    return render(request, 'admin/mascotas/eliminarMascota.html', {'mascota': mascota})


# =======================
# ABM RAZA (fbv)
# =======================
# listar -> sabri
@login_required(login_url='/login/')
def listar_razas(request):
    razas = Raza.objects.all()
    return render(request, 'admin/raza/listarRaza.html', {'razas': razas})

# crear -> cami
@login_required(login_url='/login/')
def crear_raza(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especie_id = request.POST.get('especie')

        especie = None
        if especie_id:
            especie = get_object_or_404(Especie, id=especie_id)

        nuevaRaza = Raza(nombre=nombre, especie=especie)
        nuevaRaza.save()
        return redirect('listar_razas')
    
    especies = Especie.objects.all()
    return render(request, 'admin/raza/crearRaza.html', {'especies': especies})

# eliminar -> marce
@login_required(login_url='/login/')
def eliminar_raza(request, raza_id):
    raza = get_object_or_404(Raza, id=raza_id)
    if request.method == 'POST':
        raza.delete()
        messages.success(request, "La raza ha sido eliminada exitosamente.")
        return redirect('listar_razas')
    return render(request, 'admin/raza/eliminarRaza.html', {'raza': raza})

# modificar -> jessi
@login_required(login_url='/login/')
def modificar_raza(request, raza_id):
    raza = get_object_or_404(Raza, id=raza_id)
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if form.is_valid():
            form.save()
            return redirect('listar_razas')
    else:
        form = RazaForm(instance=raza)
    return render(request, 'admin/raza/modificarRaza.html', {'form': form})


# =======================
# ABM ESPECIE (cbv)
# =======================
# crear -> jessi
class CrearEspecieView(CreateView, Restringir_acceso):
    model = Especie
    form_class = EspecieForm
    template_name = 'admin/especie/crearEspecie.html'
    success_url = reverse_lazy('listar_especies')

# eliminar -> sabri
class EliminarEspecie(DeleteView, Restringir_acceso):
    model = Especie
    template_name = 'admin/especie/eliminarEspecie.html'
    success_url = reverse_lazy('listar_especies')

# modificar -> cami
class ModificarEspecieView(UpdateView, Restringir_acceso):
    model = Especie
    form_class = EspecieForm
    template_name = 'admin/especie/modificarEspecie.html'
    success_url = reverse_lazy('listar_especies')

# listar -> marce
class ListarEspeciesView(ListView, Restringir_acceso):
    model = Especie
    template_name = 'admin/especie/listarEspecie.html'
    context_object_name = 'especies'


# =======================
# ABM PERSONA (fbv)
# =======================
# crear -> marce
@login_required(login_url='/login/')
def crear_persona(request):
    if request.method == 'POST':
        form = PersonasForm(request.POST)
        domicilio_form = DomicilioForm(request.POST)

        if form.is_valid() and domicilio_form.is_valid():
            domicilio = domicilio_form.save()
            persona = form.save(commit=False)
            persona.domicilio = domicilio
            user_id = request.POST.get("user")
            if user_id:
                persona.user = User.objects.get(id=user_id)
            persona.save()
            return redirect('listar_personas')
    else:
        form = PersonasForm()
        domicilio_form = DomicilioForm()
    return render(request, 'admin/personas/crearPersonas.html', {'form': form, 'domicilio_form': domicilio_form})

# modificar -> sabri
@login_required(login_url='/login/')
def modificar_persona(request, id):
    persona = get_object_or_404(Persona, pk=id)
    domicilio = persona.domicilio
    if request.method == 'POST':
        form = PersonasForm(request.POST, instance=persona)
        domicilio_form = DomicilioForm(request.POST, instance=domicilio)
        if form.is_valid() and domicilio_form.is_valid():
            domicilio_form.save()
            form.save()
            return redirect('listar_personas')
    else:
        form = PersonasForm(instance=persona)
        domicilio_form = DomicilioForm(instance=domicilio)
    return render(request, 'admin/personas/modificarPersona.html', {'form': form, 'domicilio_form': domicilio_form})

# baja que no puede adoptar ni registrarse -> cami
@login_required(login_url='/login/')
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)

    if request.method == 'POST':
       if persona.user is None:
            messages.error(request, "Esta persona no tiene un usuario")
            return redirect('listar_personas')
       persona.user.is_active = False
       persona.user.save()
       persona.puede_adoptar = False
       persona.save()
       return redirect('listar_personas')
    
    return render(request, 'admin/personas/bajaPersonas.html', {'persona': persona})

# alta puede adoptar y registrarse -> cami
@login_required(login_url='/login/')
def habilitar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    if request.method == 'POST':
        if persona.user is None:
            messages.error(request, "Esta persona no tiene un usuario")
            return redirect('listar_personas')
        persona.user.is_active = True
        persona.user.save()
        persona.puede_adoptar = True
        persona.save()
        return redirect('listar_personas')
    return render(request, 'admin/personas/altaPersonas.html', {'persona': persona})

def baja_persona_confirmar(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)

    if request.method == 'POST':
        if persona.user:
            persona.user.is_active = False
            persona.user.save()
        persona.puede_adoptar = False
        persona.save()
        messages.success(request, f"{persona.nombre} {persona.apellido} fue dado de baja.")
        return redirect('listar_personas')

    return render(request, 'admin/personas/bajaPersonas.html', {'persona': persona})


# listar -> jessi
@login_required(login_url='/login/')
def listar_personas(request):
    persona = Persona.objects.all()
    for p in persona:
        print("persona=" + p.nombre)
    return render(request, 'admin/personas/listaPersonas.html', {'personas': persona})


# =======================
# PERFIL DE USUARIO
# =======================
@login_required(login_url='/login/')
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'admin/edit_profile.html', {'form': form})


@login_required(login_url='/login/')
def view_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'profile': profile})


# =======================
# CORREO ELECTRÓNICO
# =======================
def generar_contraseña_temporal(longitud=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))


def recuperar_contraseña(request):
    mensaje = ""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            usuario = User.objects.get(email=email)
            nueva_pass = generar_contraseña_temporal()
            usuario.set_password(nueva_pass)
            usuario.save()
            usuario.userprofile.primer_ingreso = True
            usuario.userprofile.save()
            contexto = {"usuario": usuario.username, "nueva_pass": nueva_pass}
            contenido_html = render_to_string("correo.html", contexto)
            contenido_texto = strip_tags(contenido_html)
            enviar_correo(
                asunto="Recuperación de contraseña",
                destinatarios=[email],
                texto=contenido_texto,
                html=contenido_html
            )
            mensaje = "Se ha enviado una nueva contraseña a tu correo."
        except User.DoesNotExist:
            mensaje = "No existe un usuario con ese correo."
    return render(request, "contraseña/recu_contraseña.html", {"mensaje": mensaje})


# =======================
# CAMBIO DE CONTRASEÑA
# =======================
@login_required(login_url='/login/')
def cambiar_password(request, id):
    perfil = UserProfile.objects.get(id=id)
    if not perfil.primer_ingreso:
        return redirect('dashboard')
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('password')
        confirmar_contraseña = request.POST.get('password2')
        if nueva_contraseña == confirmar_contraseña:
            perfil.user.set_password(nueva_contraseña)
            perfil.user.save()
            perfil.primer_ingreso = False
            perfil.save()
            messages.success(request, "Tu contraseña se cambió con éxito, volvé a iniciar sesión")
            return redirect('login')
        else:
            mensaje = "Las contraseñas no coinciden."
            return render(request, 'contraseña/cambiarContraseña.html', {'mensaje': mensaje})
    return render(request, 'contraseña/cambiarContraseña.html')


@login_required(login_url='/login/')
def cambiar_contraseña_voluntariamente(request):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('password')
        confirmar = request.POST.get('password2')
        if nueva_contraseña == confirmar:
            request.user.set_password(nueva_contraseña)
            request.user.save()
            messages.success(request, "Tu contraseña se cambió con éxito, volvé a iniciar sesión")
            return redirect('login')
        else:
            messages.error(request, "Lo lamento, las contraseñas no coinciden")
    return render(request, 'contraseña/cambiarContraseña.html')


# =======================
# FILTRO DE MASCOTAS
# =======================
@login_required(login_url='/login/')
def filtrar_mascotas(request):
    # Listas completas
    razas = Raza.objects.all()
    especies = Especie.objects.all()
    localidades = Localidad.objects.all()

    # Parámetros GET para filtrado
    
    selected_raza = request.GET.get('raza')
    selected_especie = request.GET.get('especie')
    selected_localidad = request.GET.get('localidad')

    # Query inicial de mascotas
    mascotas = Mascotas.objects.all()

    # Filtrados condicionales
    if selected_raza:
        mascotas = mascotas.filter(raza_id=int(selected_raza))
        
    if selected_especie:
        mascotas = mascotas.filter(raza__especie_id=int(selected_especie))
        razas = razas.filter(especie_id=selected_especie)


    if selected_localidad:
        mascotas = mascotas.filter(localidad_id=int(selected_localidad))

    # Contexto
    context = {
        'especies': especies,
        'razas': razas,
        'localidades': localidades,
        'mascotas': mascotas,
        'selected_especie': int(selected_especie) if selected_especie else None,
        'selected_raza': int(selected_raza) if selected_raza else None,
        'selected_localidad': int(selected_localidad) if selected_localidad else None,
    }

    return render(request, 'user/detalle_mascotas.html', context)


# =======================
# EXPLORAR ESPECIES Y RAZAS (sabri)
# =======================
@login_required(login_url='/login/')
def explorar_especies(request):

    especies = Especie.objects.prefetch_related('razas').all()
    
    # Diccionario de íconos por especie
    iconos = {
        "Perro": "fa-dog",
        "Gato": "fa-cat",
        "Ave": "fa-dove",
        "Conejo": "fa-carrot",
        "Pez": "fa-fish",
        "Reptil": "fa-dragon",
        "roedor": "fa-mouse"
    }

    context = {
         "especies":[          
         {
                "obj": e.nombre,
                "icono": iconos.get(e.nombre, "fa-paw"),  # o tu función de iconos
                "razas": e.razas.all(),
            }
            for e in especies
        ]
    }
    return render(request, "user/explorar_especies.html", context)


@login_required(login_url='/login/')
@login_required(login_url='/login/')
def explorar_razas(request, raza_id):
    # Obtengo la raza
    raza = get_object_or_404(Raza, id=raza_id)
    especie = raza.especie

    # Obtengo todas las mascotas de esa raza
    mascotas = Mascotas.objects.filter(raza=raza)

    contexto = {
        "especie": especie,
        "raza": raza,
        "mascotas": mascotas,  # 👈 esto es lo que detalle_mascotas.html necesita
    }

    return render(request, 'user/detalle_mascotas.html', contexto)


# =======================
# MÓDULO ADOPCIONES (sabri)
# =======================
@login_required(login_url='/login/')
def mis_adopciones(request):
    adopciones_qs = Adopcion.objects.filter(usuario=request.user)

    adopciones = []
    for a in adopciones_qs:
        adopciones.append({
            "mascota": a.mascota,
            "especie": a.mascota.raza.especie.nombre,
            "raza": a.mascota.raza.nombre,
            "fecha": a.fecha_adopcion,
            "seguimiento": a.seguimiento,  # si tienes un campo booleano o texto
        })

    # Mensaje si no hay adopciones
    if not adopciones:
        storage = messages.get_messages(request)
        if not any(msg.message == "Todavía no realizaste ninguna adopción." for msg in storage):
            messages.info(request, "Todavía no realizaste ninguna adopción.")

    context = {
        "adopciones": adopciones
    }

    return render(request, 'user/mis_adopciones.html', context)

@login_required(login_url='/login/')
def detalle_mascota(request, mascota_id):
    """
    Página de detalle de una mascota.
    Muestra foto, nombre, raza/especie, sexo, localidad, descripción y botones.
    """
    mascota = get_object_or_404(Mascotas, id=mascota_id)

    # Información segura (no asumimos que existan todos los campos)
    foto_url = mascota.foto.url if getattr(mascota, "foto", None) and getattr(mascota.foto, "url", None) else None
    nombre = getattr(mascota, "nombre", "Sin nombre")
    descripcion = getattr(mascota, "descripcion", "")  # si tu modelo no tiene 'descripcion' puede estar vacío
    sexo = getattr(mascota, "sexo", None)  # si tenés SEXO_CHOICES
    raza = getattr(mascota, "raza", None)
    localidad = getattr(mascota, "localidad", None)

    contexto = {
        "mascota": mascota,
        "foto_url": foto_url,
        "nombre": nombre,
        "descripcion": descripcion,
        "sexo": sexo,
        "raza": raza,
        "localidad": localidad,
    }

    return render(request, "user/detalle_mascota.html", contexto)






























"""
def cambiar_password(request, token):
    try:
        profile = UserProfile.objects.get(recovery_token=token)
        if request.method == 'POST':
            nueva_password = request.POST.get('password')
            profile.user.password = make_password(nueva_password)
            profile.user.save()
            profile.recovery_token = ''  # Limpiar token
            profile.save()
            return render(request, 'password_cambiada.html')
        return render(request, 'cambiar_password.html')
    except UserProfile.DoesNotExist:
        return render(request, 'token_invalido.html')
    """