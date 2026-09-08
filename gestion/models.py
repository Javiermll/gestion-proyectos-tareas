from django.conf import settings
from django.db import models

# Clase que representa un proyecto que crea un usuario.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)   # Nombre corto del proyecto, obligatorio.
    descripcion = models.TextField(blank=True)  # Descripción: opcional (blank=True no es obligatorio llenarlo)

    # Se conecta con el modelo de usuario de Django (User) para saber a qué usuario pertenece el proyecto.
    # settings.AUTH_USER_MODEL en vez de importar User directo, porque es la forma recomendada
    # on_delete=models.CASCADE significa: si se borra el usuario, se borran también sus proyectos
    # related_name me permite después escribir usuario.proyectos.all() para traer todos sus proyectos
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proyectos',
    )

    # auto_now_add=True hace que Django guarde la fecha automáticamente solo la primera vez
    creado_en = models.DateTimeField(auto_now_add=True)

    # Esto es lo que se muestra cuando imprimo un objeto Proyecto (por ejemplo en el panel admin)
    def __str__(self):
        return self.nombre


# Clase que representa una tarea dentro de un proyecto.
# Cada tarea tiene un estado (en qué etapa va) y una prioridad (qué tan urgente es)
class Tarea(models.Model):

    # Opciones posibles para el estado de la tarea
    # TextChoices define opciones fijas. 
    class Estado(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente'
        EN_PROGRESO = 'PRO', 'En progreso'
        COMPLETADA = 'COM', 'Completada'

    # Lo mismo pero para la prioridad
    class Prioridad(models.TextChoices):
        BAJA = 'BAJ', 'Baja'
        MEDIA = 'MED', 'Media'
        ALTA = 'ALT', 'Alta'

    # Título corto de la tarea, obligatorio
    titulo = models.CharField(max_length=150)

    # Descripción más detallada, opcional
    descripcion = models.TextField(blank=True)

    # Cada tarea pertenece a un proyecto (relación uno a muchos)
    # related_name='tareas' me permite después escribir proyecto.tareas.all()
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='tareas',
    )

    # Guardo el estado como texto corto (PEN, PRO o COM)
    # valor por defecto para que las tareas nuevas empiecen como pendientes
    estado = models.CharField(
        max_length=3,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    # Lo mismo para la prioridad, con valor por defecto medio
    prioridad = models.CharField(
        max_length=3,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )

    # Fecha de creación, se guarda sola la primera vez
    creado_en = models.DateTimeField(auto_now_add=True)

    # Lo que se muestra al imprimir la tarea, por ejemplo en el panel admin
    def __str__(self):
        return self.titulo