from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Proyecto, Tarea  #Se agrega tarea y proyecto.


#### Vista: resumen inicial (dashboard) con los números y novedades del usuario
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # mismo filtro de siempre: cada usuario solo ve lo suyo
        proyectos = Proyecto.objects.filter(propietario=self.request.user)
        tareas = Tarea.objects.filter(proyecto__propietario=self.request.user)

        context['total_proyectos'] = proyectos.count()
        context['total_pendientes'] = tareas.filter(estado=Tarea.Estado.PENDIENTE).count()
        context['total_progreso'] = tareas.filter(estado=Tarea.Estado.EN_PROGRESO).count()
        context['total_completadas'] = tareas.filter(estado=Tarea.Estado.COMPLETADA).count()

        # solo los más nuevos, para no repetir el listado completo que ya está en /proyectos/ y /tareas/
        context['proyectos_recientes'] = proyectos.order_by('-creado_en')[:3]
        context['tareas_recientes'] = tareas.order_by('-creado_en')[:5]

        return context

#### Vista: registro de un usuario nuevo
def registro(request):
    if request.method == 'POST': # Si el usuario envió el formulario (método POST), lo proceso
        form = UserCreationForm(request.POST) # UserCreationForm ya viene con Django y valida usuario + contraseña + confirmación
        if form.is_valid():  # is_valid() revisa que los datos cumplan las reglas (contraseñas coincidan, etc.)
            form.save()      # save() crea el usuario nuevo en la base de datos
            return redirect('login') # después de registrarse, lo mando directo a la página de login
    else:
        form = UserCreationForm()  # si el usuario solo entró a la página (método GET), le muestro el formulario vacío

    return render(request, 'gestion/registro.html', {'form': form})  # le paso el formulario al template para que lo dibuje en pantalla


#### Vista: lista de proyectos
# LoginRequiredMixin hace que si alguien no inició sesión, Django lo mande solo al login
class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'gestion/proyectos/proyecto_list.html'  # ruta actualizada con subcarpeta proyectos/
    context_object_name = 'proyectos'  # así se va a llamar la variable dentro del template
    paginate_by = 6  # 2 filas de 3 tarjetas por página

    # Método para que solo traiga los proyectos del usuario que inició sesión
    # el orden explícito es necesario para que la paginación sea consistente entre páginas
    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user).order_by('-creado_en')


# Vista: formulario para crear un proyecto nuevo
class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    fields = ['nombre', 'descripcion']  # campos que va a mostrar el formulario
    template_name = 'gestion/proyectos/proyecto_form.html'  # ruta actualizada con subcarpeta proyectos/
    success_url = reverse_lazy('proyecto_list')  # a dónde va después de crear

    # este método se ejecuta justo antes de guardar el formulario
    # lo uso para asignar el propietario automáticamente, sin que el usuario lo elija
    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)


# Vista: formulario para editar un proyecto existente
class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    fields = ['nombre', 'descripcion']
    template_name = 'gestion/proyectos/proyecto_form.html'  # ruta actualizada con subcarpeta proyectos/
    success_url = reverse_lazy('proyecto_list')

    # esto evita que un usuario edite el proyecto de otro cambiando el número en la url
    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)


# Vista: confirmación y luego elimina el proyecto
class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'gestion/proyectos/proyecto_confirm_delete.html'  # ruta actualizada con subcarpeta proyectos/
    success_url = reverse_lazy('proyecto_list')

    # mismo cuidado que en la vista de editar: solo puede borrar lo suyo
    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)

#### Vista: lista de tareas
# igual que con Proyecto, solo entra quien inició sesión
class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'gestion/tareas/tarea_list.html'  # ruta actualizada con subcarpeta tareas/
    context_object_name = 'tareas'
    paginate_by = 8  # tareas por página

    #En simple: solo traigo las tareas cuyo proyecto pertenece al usuario que inició sesión.
    # el orden explícito es necesario para que la paginación sea consistente entre páginas
    def get_queryset(self):
        return Tarea.objects.filter(proyecto__propietario=self.request.user).order_by('-creado_en')


# Vista: formulario para crear una tarea nueva
class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'proyecto', 'estado', 'prioridad']
    template_name = 'gestion/tareas/tarea_form.html'  # ruta actualizada con subcarpeta tareas/
    success_url = reverse_lazy('tarea_list')

    # acá restrinjo las opciones del campo "proyecto" en el formulario
    # para que el usuario solo pueda elegir entre sus propios proyectos, no los de otros
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['proyecto'].queryset = Proyecto.objects.filter(propietario=self.request.user)
        return form


# Vista: formulario para editar una tarea existente
class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'proyecto', 'estado', 'prioridad']
    template_name = 'gestion/tareas/tarea_form.html'  # ruta actualizada con subcarpeta tareas/
    success_url = reverse_lazy('tarea_list')

    # mismo filtro que en creación: no puede asignar la tarea a un proyecto ajeno
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['proyecto'].queryset = Proyecto.objects.filter(propietario=self.request.user)
        return form

    # y esto evita que edite una tarea que no es suya, cambiando el número en la url
    def get_queryset(self):
        return Tarea.objects.filter(proyecto__propietario=self.request.user)


# Vista: confirmación y luego elimina la tarea
class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'gestion/tareas/tarea_confirm_delete.html'  # ruta actualizada con subcarpeta tareas/
    success_url = reverse_lazy('tarea_list')

    def get_queryset(self):
        return Tarea.objects.filter(proyecto__propietario=self.request.user)