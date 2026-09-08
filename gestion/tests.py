from django.test import TestCase
from django.contrib.auth.models import User
from .models import Proyecto, Tarea
from django.urls import reverse

# esta clase agrupa todos los tests relacionados al modelo Proyecto
class ProyectoModelTest(TestCase):

    # setUp se ejecuta antes de cada test de esta clase, sirve para preparar datos de prueba
    def setUp(self):
        # creo un usuario de prueba, porque Proyecto necesita un propietario obligatorio
        self.usuario = User.objects.create_user(username='testuser', password='clave12345')

    # cada método que empieza con "test_" es un caso de prueba independiente
    def test_creacion_proyecto(self):
        # creo un proyecto de prueba, asignado al usuario de arriba
        proyecto = Proyecto.objects.create(
            nombre='Proyecto de prueba',
            descripcion='Una descripción cualquiera',
            propietario=self.usuario,
        )

        # assertEqual revisa que el valor guardado sea el que yo esperaba
        self.assertEqual(proyecto.nombre, 'Proyecto de prueba')
        self.assertEqual(proyecto.propietario, self.usuario)

    def test_str_proyecto(self):
        # este test revisa que el método __str__ del modelo devuelva el nombre, como definimos en la fase 2
        proyecto = Proyecto.objects.create(nombre='Otro proyecto', propietario=self.usuario)
        self.assertEqual(str(proyecto), 'Otro proyecto')


# esta clase agrupa los tests del modelo Tarea
class TareaModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='testuser2', password='clave12345')
        # las tareas necesitan un proyecto, así que creo uno primero
        self.proyecto = Proyecto.objects.create(nombre='Proyecto base', propietario=self.usuario)

    def test_creacion_tarea_con_valores_por_defecto(self):
        # creo una tarea sin especificar estado ni prioridad, para revisar que tome los valores por defecto
        tarea = Tarea.objects.create(titulo='Tarea de prueba', proyecto=self.proyecto)

        # reviso que haya tomado los valores por defecto que definimos en el modelo (fase 2)
        self.assertEqual(tarea.estado, Tarea.Estado.PENDIENTE)
        self.assertEqual(tarea.prioridad, Tarea.Prioridad.MEDIA)

    def test_relacion_tarea_proyecto(self):
        # este test revisa que related_name='tareas' funcione como esperamos
        Tarea.objects.create(titulo='Tarea 1', proyecto=self.proyecto)
        Tarea.objects.create(titulo='Tarea 2', proyecto=self.proyecto)

        # gracias a related_name, puedo acceder a las tareas de un proyecto así
        self.assertEqual(self.proyecto.tareas.count(), 2)



# esta clase agrupa los tests de las vistas de Proyecto
class ProyectoViewTest(TestCase):

    def setUp(self):
        # creo dos usuarios distintos, para probar que no se mezclen sus datos
        self.usuario1 = User.objects.create_user(username='usuario1', password='clave12345')
        self.usuario2 = User.objects.create_user(username='usuario2', password='clave12345')

        # este proyecto le pertenece solo al usuario1
        self.proyecto_usuario1 = Proyecto.objects.create(nombre='Proyecto de usuario1', propietario=self.usuario1)

    def test_redirige_a_login_si_no_hay_sesion(self):
        # intento entrar a la lista de proyectos SIN haber iniciado sesión
        respuesta = self.client.get(reverse('proyecto_list'))

        # 302 significa "redirección", justo lo que esperamos que pase (te manda al login)
        self.assertEqual(respuesta.status_code, 302)

    def test_usuario_ve_solo_sus_propios_proyectos(self):
        # inicio sesión como usuario2, que no tiene ningún proyecto propio
        self.client.login(username='usuario2', password='clave12345')

        respuesta = self.client.get(reverse('proyecto_list'))

        # reviso que el proyecto de usuario1 NO aparezca en el contexto que le llega a usuario2
        # esto prueba que get_queryset() está filtrando correctamente
        self.assertNotIn(self.proyecto_usuario1, respuesta.context['proyectos'])

    def test_usuario_no_puede_editar_proyecto_ajeno(self):
        # inicio sesión como usuario2, e intento editar el proyecto que es de usuario1
        self.client.login(username='usuario2', password='clave12345')

        url = reverse('proyecto_update', args=[self.proyecto_usuario1.pk])
        respuesta = self.client.get(url)

        # 404 es la respuesta correcta acá: como get_queryset() filtra por propietario,
        # Django no encuentra el proyecto (no es que lo encuentre y lo bloquee, directamente no existe para usuario2)
        self.assertEqual(respuesta.status_code, 404)

    def test_creacion_proyecto_asigna_propietario_automaticamente(self):
        # inicio sesión como usuario1 y envío el formulario de creación
        self.client.login(username='usuario1', password='clave12345')

        respuesta = self.client.post(reverse('proyecto_create'), {
            'nombre': 'Proyecto nuevo desde test',
            'descripcion': 'Creado durante un test',
        })

        # reviso que el proyecto se haya creado y que su propietario sea automáticamente usuario1
        # esto prueba que form_valid() en ProyectoCreateView funciona como esperamos (fase 4)
        proyecto_creado = Proyecto.objects.get(nombre='Proyecto nuevo desde test')
        self.assertEqual(proyecto_creado.propietario, self.usuario1)

# esta clase agrupa los tests de las vistas de Tarea
class TareaViewTest(TestCase):

    def setUp(self):
        self.usuario1 = User.objects.create_user(username='usuario1t', password='clave12345')
        self.usuario2 = User.objects.create_user(username='usuario2t', password='clave12345')

        # este proyecto y esta tarea le pertenecen solo al usuario1
        self.proyecto_usuario1 = Proyecto.objects.create(nombre='Proyecto de usuario1', propietario=self.usuario1)
        self.tarea_usuario1 = Tarea.objects.create(titulo='Tarea de usuario1', proyecto=self.proyecto_usuario1)

    def test_redirige_a_login_si_no_hay_sesion(self):
        # mismo chequeo que en Proyecto: sin sesión, debe redirigir (302), no mostrar la lista
        respuesta = self.client.get(reverse('tarea_list'))
        self.assertEqual(respuesta.status_code, 302)

    def test_usuario_ve_solo_sus_propias_tareas(self):
        # inicio sesión como usuario2, que no tiene ninguna tarea propia
        self.client.login(username='usuario2t', password='clave12345')

        respuesta = self.client.get(reverse('tarea_list'))

        # la tarea de usuario1 no debería aparecer en el contexto que recibe usuario2
        self.assertNotIn(self.tarea_usuario1, respuesta.context['tareas'])

    def test_usuario_no_puede_editar_tarea_ajena(self):
        # inicio sesión como usuario2, e intento editar la tarea que es de usuario1
        self.client.login(username='usuario2t', password='clave12345')

        url = reverse('tarea_update', args=[self.tarea_usuario1.pk])
        respuesta = self.client.get(url)

        # 404 porque get_queryset() filtra por proyecto__propietario, así que Django no la encuentra
        self.assertEqual(respuesta.status_code, 404)

    def test_formulario_creacion_solo_muestra_proyectos_propios(self):
        # este test es específico de Tarea: revisa que el campo "proyecto" del formulario
        # solo ofrezca los proyectos de quien inició sesión, no los de otros usuarios (lo definimos en get_form(), fase 4)
        self.client.login(username='usuario2t', password='clave12345')

        # creo un proyecto que sí le pertenece a usuario2, para comparar
        proyecto_usuario2 = Proyecto.objects.create(nombre='Proyecto de usuario2', propietario=self.usuario2)

        respuesta = self.client.get(reverse('tarea_create'))
        opciones_proyecto = respuesta.context['form'].fields['proyecto'].queryset

        # el proyecto de usuario2 sí debe aparecer como opción
        self.assertIn(proyecto_usuario2, opciones_proyecto)

        # pero el proyecto de usuario1 NO debe aparecer como opción
        self.assertNotIn(self.proyecto_usuario1, opciones_proyecto)