from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.conf import settings

class Provincia(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "La provincia es: " + self.descripcion

class Localidad(models.Model):
    descripcion = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="localidades")

    class Meta:
        unique_together = ('descripcion', 'provincia')  
        
    def __str__(self):
        return f"{self.descripcion} ({self.provincia})"


class Domicilio(models.Model):
    calle = models.CharField(max_length=120)
    numero = models.CharField(max_length=10, blank=True, null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, related_name="domicilios")
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.calle} {self.numero or ''}, {self.localidad}"


class Persona(models.Model):
    apellido = models.CharField(max_length=80)
    nombre = models.CharField(max_length=80)
    dni = models.CharField("Documento", max_length=20, blank=True, null=True, unique=True)
    fecha_nacimiento = models.DateField()
    domicilio = models.ForeignKey(Domicilio, on_delete=models.SET_NULL, null=True, blank=True, related_name="personas")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # <-- nuevo campo para asociar usuario
    puede_adoptar = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Especie(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(default="")

    def __str__(self):
        return f"{self.nombre}"

class Raza(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, null=True, blank=True, related_name="razas")
    nombre = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.nombre}"

SEXO_CHOICES = (
    ("Macho", "Macho"), 
    ("Hembra", "Hembra"),
)

class Mascotas(models.Model):
    raza = models.ForeignKey(Raza, on_delete=models.SET_NULL, null=True, blank=True, related_name="mascotas")
    sexo = models.CharField(max_length= 6, choices = SEXO_CHOICES)
    tamanio = models.CharField(max_length=80)
    observaciones = models.CharField(max_length=200)
    fecha_nac = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    fotos = models.ImageField(upload_to='mascotas/', blank=True, null=True) #nuevo campo para agregar imagenes
    estado_inicial=models.CharField(max_length=200, blank=True, null=True)#estado inicial para el seguimiento de adopcion

    def __str__(self):
       
        especie_nombre = self.raza.especie.nombre if self.raza and self.raza.especie else "Sin especie"
        raza_nombre = self.raza.nombre if self.raza else "Sin raza"
        return f"{especie_nombre}, {raza_nombre}, {self.sexo}, {self.tamanio}, {self.fecha_nac}, {self.observaciones}"


#INSERCION DE IMAGENES  // CORREO (extendimos este modelo agregando el campo "primer ingreso")
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to = 'avatars/', default='avatars/default.png')
    primer_ingreso = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
#Django lo ejecuta automaticamente, cada vez que se cree un User se crea tambien su UserProfile
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, primer_ingreso=False)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.userprofile.save()
class SolicitudAdopcion(models.Model):
    ESTADO_CHOICES = [
        ('iniciada', 'Iniciada'),
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mascota = models.ForeignKey('Mascotas', on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True)    # info adicional del solicitante
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    respuesta_admin = models.TextField(blank=True)     # texto de aprobación/rechazo del admin
    procesada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='procesadas')  # admin que procesa

    class Meta:
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud #{self.id} - {self.mascota} - {self.usuario}"
class Adopcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    fecha_adopcion = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    solicitud=models.OneToOneField(SolicitudAdopcion, null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.usuario.username} adoptó a {self.mascota}"

class ContactMessage(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.email}"

#===MODELO PARA CREAR NOTICIAS/NOVEDADES DESDE EL ADMIN Y QUE SE VEAN PUBLICAMENTE===#
class Novedad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion_corta = models.TextField(max_length=300)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="novedades/", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']  # más nuevas primero

    def __str__(self):
        return self.titulo
    
#para el seguimiento de adopcion
class ObservacionesSeguimiento(models.Model):
    mascota=models.ForeignKey(Mascotas, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=200)
    fecha=models.DateField(auto_now_add=True)
    detalle=models.TextField()

class VacunasSeguimiento(models.Model):
    mascota=models.ForeignKey(Mascotas,on_delete=models.CASCADE)
    nombre_vacuna=models.CharField(max_length=100)
    fecha_puesta=models.DateField(auto_now_add=True)
    proxima_dosis=models.DateField(null=True, blank=True)