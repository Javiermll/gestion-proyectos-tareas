from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Vista de login que ya viene incluida en Django. Se le indica que template usar para mostrar el formulario
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Esta es la vista de logout (incluida)
    path('registro/', views.registro, name='registro'), # Vista de registro

    # resumen inicial con los números del usuario (proyectos, tareas por estado, etc.)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # rutas nuevas para el CRUD de proyectos
    path('proyectos/', views.ProyectoListView.as_view(), name='proyecto_list'),
    path('proyectos/nuevo/', views.ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyectos/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyectos/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='proyecto_delete'),

    # rutas nuevas para el CRUD de tareas
    path('tareas/', views.TareaListView.as_view(), name='tarea_list'),
    path('tareas/nueva/', views.TareaCreateView.as_view(), name='tarea_create'),
    path('tareas/<int:pk>/editar/', views.TareaUpdateView.as_view(), name='tarea_update'),
    path('tareas/<int:pk>/eliminar/', views.TareaDeleteView.as_view(), name='tarea_delete'),
]