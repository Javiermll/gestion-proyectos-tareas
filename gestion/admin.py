from django.contrib import admin
from .models import Proyecto, Tarea

# esta clase le dice al admin cómo mostrar la lista de proyectos
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'propietario', 'creado_en'] # Columnas que se ven en la lista, en vez de solo el nombre
    search_fields = ['nombre']  # Buscador arriba de la lista, para buscar por nombre
    list_filter = ['propietario'] # Filtros a la derecha, para filtrar por propietario


# lo mismo pero para tareas
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'estado', 'prioridad', 'creado_en']
    list_filter = ['estado', 'prioridad']  # filtrar por estado y prioridad.
    search_fields = ['titulo']


# Registro los modelos Proyecto y Tarea para que se puedan administrar desde el panel de administración de Django, 
# usando las clases ProyectoAdmin y TareaAdmin para personalizar su apariencia y funcionalidad.
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Tarea, TareaAdmin)