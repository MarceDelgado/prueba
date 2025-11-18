from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.core.models import Especie, Mascotas, Raza, Persona, Adopcion
from .forms import EspecieForm, RazaForm, RegistroUsuarioForm, MascotasForm, PersonasForm, DomicilioForm, UserProfileForm, SolicitudAdopcionForm
from django.contrib.auth import authenticate, login, logout as auth_logout  # importamos la funcion "authenticate"
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View  # importamos las clases bases para el abm
from .models import Localidad, UserProfile, SolicitudAdopcion

# correo
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .emails import enviar_correo
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import mail_admins

from django.contrib.auth.hashers import make_password
import random, string

# decoradores
from django.contrib.auth.decorators import login_required  # -> para fbv
from django.utils.decorators import method_decorator  # -> para cbv


# =======================
# PÁGINAS PÚBLICAS
# =======================
def home(request):
    # Las 5 mascotas más recientes (suponiendo que tu modelo tenga un campo fecha o id autoincremental)
    mascotas_recientes = Mascotas.objects.order_by('-created_at')[:5]

    return render(request, "home.html", {
        'mascotas': mascotas_recientes
    })

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
            return redirect('home')
       else:
            mensaje = 'usuario y/o contraseña incorrecta'
            contexto = {'mensaje': mensaje}
            return render(request, 'login.html', contexto)
   return render(request, 'login.html')


def dashboard(request):
    
    return render(request, 'home.html', {})


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
    template_name = 'user/detalle_mascotas.html'
    context_object_name = 'mascotas'
    
    def get_queryset(self):
        mascotas = super().get_queryset()  # equivale a Mascotas.objects.all()

        raza_id = self.request.GET.get("raza")
        if raza_id:
            mascotas = mascotas.filter(raza_id=raza_id)

        return mascotas
        
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
# listar 
@login_required(login_url='/login/')
def listar_razas(request):
    razas = Raza.objects.all()
    return render(request, 'admin/raza/listarRaza.html', {'razas': razas})

# crear 
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

# eliminar 
@login_required(login_url='/login/')
def eliminar_raza(request, raza_id):
    raza = get_object_or_404(Raza, id=raza_id)
    if request.method == 'POST':
        raza.delete()
        messages.success(request, "La raza ha sido eliminada exitosamente.")
        return redirect('listar_razas')
    return render(request, 'admin/raza/eliminarRaza.html', {'raza': raza})

# modificar
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
# crear 
class CrearEspecieView(CreateView, Restringir_acceso):
    model = Especie
    form_class = EspecieForm
    template_name = 'admin/especie/crearEspecie.html'
    success_url = reverse_lazy('listar_especies')

# eliminar
class EliminarEspecie(DeleteView, Restringir_acceso):
    model = Especie
    template_name = 'admin/especie/eliminarEspecie.html'
    success_url = reverse_lazy('listar_especies')

# modificar
class ModificarEspecieView(UpdateView, Restringir_acceso):
    model = Especie
    form_class = EspecieForm
    template_name = 'admin/especie/modificarEspecie.html'
    success_url = reverse_lazy('listar_especies')

# listar
class ListarEspeciesView(ListView, Restringir_acceso):
    model = Especie
    template_name = 'admin/especie/listarEspecie.html'
    context_object_name = 'especies'

# =======================
# ABM PERSONA (fbv)
# =======================
# crear
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

# modificar
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

# baja que no puede adoptar ni registrarse
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

# alta puede adoptar y registrarse
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

# listar 
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
# EXPLORAR MASCOTAS, ESPECIES Y RAZAS
# =======================
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
# MÓDULO ADOPCIONES
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

@login_required(login_url='/login/')
def formulario_adopcion(request, mascota_id):
    mascota = get_object_or_404(Mascotas, id=mascota_id)

    # Evitar duplicados: opcional, por ejemplo no permitir más de una solicitud pendiente por el mismo usuario/mascota
    pendiente = SolicitudAdopcion.objects.filter(usuario=request.user, mascota=mascota, estado='pendiente').exists()
    if pendiente:
        messages.info(request, "Ya tenés una solicitud pendiente para esta mascota.")
        return redirect('detalle_mascota', mascota_id=mascota.id)

    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.mascota = mascota
            solicitud.save()

            # Notificar a administradores (usa settings.ADMINS)
            subject = f"Nueva solicitud de adopción: {mascota.nombre} (id {solicitud.id})"
            message = (
                f"Usuario: {request.user.get_full_name() or request.user.username}\n"
                f"Email: {request.user.email}\n"
                f"Teléfono: {solicitud.telefono}\n"
                f"Dirección: {solicitud.direccion}\n\n"
                f"Mensaje:\n{solicitud.mensaje}\n\n"
                f"Ver en admin: /admin/{solicitud._meta.app_label}/{solicitud._meta.model_name}/{solicitud.id}/change/\n"
            )
            # mail_admins envía a la lista en settings.ADMINS
            try:
                mail_admins(subject, message)
            except Exception:
                # fallback: no romper si no está configurado el email
                pass

            messages.success(request, "Tu solicitud se envió correctamente. Los administradores la evaluarán y te contactarán.")
            return redirect('mis_adopciones')  # o a donde prefieras
    else:
        # prellenar datos del usuario si existen (si querés)
        initial = {}
        profile = getattr(request.user, 'userprofile', None)
        if profile:
            # si tenés campos en el profile para telefono/direccion
            if getattr(profile, 'telefono', None):
                initial['telefono'] = profile.telefono
            if getattr(profile, 'direccion', None):
                initial['direccion'] = profile.direccion

        form = SolicitudAdopcionForm(initial=initial)

    return render(request, 'user/formulario_adopcion.html', {'form': form, 'mascota': mascota})

#@staff_member_required
def procesar_solicitud(request, pk):
    s = get_object_or_404(SolicitudAdopcion, pk=pk)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        respuesta = request.POST.get('respuesta', '')
        if accion == 'aprobar':
            s.estado = 'aprobada'
        elif accion == 'rechazar':
            s.estado = 'rechazada'
        s.respuesta_admin = respuesta
        s.procesada_por = request.user
        s.save()

        # notificar al usuario (opcional)
        try:
            from django.core.mail import send_mail
            send_mail(
                f"Tu solicitud #{s.id} ha sido {s.get_estado_display()}",
                f"Hola {s.usuario.get_full_name() or s.usuario.username},\n\n"
                f"Tu solicitud para adoptar {s.mascota.nombre} ha sido {s.estado}.\n\n"
                f"Comentario del admin:\n{respuesta}",
                None,  # from_email: None -> usa DEFAULT_FROM_EMAIL
                [s.usuario.email],
                fail_silently=True,
            )
        except Exception:
            pass

        return redirect('lista_solicitudes')

    return render(request, 'core/procesar_solicitud.html', {'s': s})

def contacto_submit(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # notificar admin
            try:
                mail_admins(
                  subject=f"Nueva consulta #{msg.id} - {msg.nombre}",
                  message=msg.mensaje + f"\n\nEmail: {msg.email}\nTel: {msg.telefono}"
                )
            except Exception:
                pass
            messages.success(request, "Gracias, tu consulta fue enviada. Te contactaremos pronto.")
            return redirect('home')
    else:
        form = ContactMessageForm()
    return render(request, 'core/contacto_form.html', {'form': form})




























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