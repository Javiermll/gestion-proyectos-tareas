# Gestión de Proyectos y Tareas — Django Web App

**Proyecto:** Evaluación del Módulo 6 — Bootcamp Full Stack Python Trainee (Talento Digital / Alkemy)

## Descripción

Aplicación web desarrollada en Django que permite a los usuarios registrarse, autenticarse, y gestionar sus propios proyectos y tareas de forma segura y aislada entre usuarios. Modela un flujo de trabajo simple tipo "task manager": cada usuario administra sus propios proyectos, y cada proyecto agrupa tareas con estado (Pendiente / En progreso / Completada) y prioridad (Baja / Media / Alta).

## 📦 Repositorio

Ver repositorio en GitHub: [github.com/Javiermll/django-gestion-proyectos-tareas](https://github.com/Javiermll/django-gestion-proyectos-tareas)

> El enlace a la versión en vivo (desplegada en Render) se agregará en esta sección.

## 🛠️ Stack Tecnológico

- Python 3.10+
- Django 6.1
- SQLite en desarrollo (o Postgres en producción, vía `DATABASE_URL`)
- Bootstrap 5 (vía CDN) + hoja de estilos propia (sistema visual "SaaS moderno")
- django-widget-tweaks (estilos en formularios generados por Django)
- python-dotenv (variables de entorno)
- gunicorn + whitenoise + dj-database-url (servidor y estáticos en producción)

## 🎯 Alcance del proyecto

Requisitos de la consigna cubiertos:

- ✅ Registro y autenticación de usuarios con `django.contrib.auth`
- ✅ Modelos `Proyecto` y `Tarea` con relaciones entre usuario, proyectos y tareas
- ✅ Templates con herencia (`base.html`), formularios con `ModelForm` y contextos dinámicos
- ✅ Sitio administrativo personalizado (`list_display`, `search_fields`, `list_filter`)
- ✅ Protección CSRF, `LoginRequiredMixin` y validación de datos
- ✅ Pruebas unitarias para modelos y vistas principales
- ✅ Documentación en README con instalación y uso

Sobre lo mínimo pedido, se sumaron por decisión propia: dashboard/resumen inicial, paginación en los listados, páginas de error personalizadas (404/500), un sistema visual propio sobre Bootstrap, y configuración lista para desplegar en producción (Render).

## 🗂️ Estructura del proyecto

```
Proy_django_gestion_tareas/
├── core/                       # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── gestion/                    # App principal con la lógica de negocio
│   ├── migrations/
│   ├── static/
│   │   └── gestion/
│   │       └── css/
│   │           └── style.css   # Hoja de estilos propia
│   ├── templates/
│   │   ├── 404.html            # Página de error personalizada
│   │   ├── 500.html            # Página de error personalizada
│   │   └── gestion/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── registro.html
│   │       ├── dashboard.html
│   │       ├── proyectos/
│   │       │   ├── proyecto_list.html
│   │       │   ├── proyecto_form.html
│   │       │   └── proyecto_confirm_delete.html
│   │       └── tareas/
│   │           ├── tarea_list.html
│   │           ├── tarea_form.html
│   │           └── tarea_confirm_delete.html
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── .env                        # Variables de entorno (no se sube al repositorio)
├── .gitignore
├── manage.py
├── requirements.txt            # Dependencias, incluidas las de producción
├── render.yaml                 # Blueprint de despliegue en Render
└── README.md
```

## ✨ Funcionalidades

- Registro, login y logout de usuarios.
- CRUD completo de **Proyecto** (nombre, descripción, propietario) y **Tarea** (título, descripción, proyecto, estado, prioridad), ambos con listados paginados.
- Aislamiento total de datos: cada usuario ve y gestiona únicamente sus propios proyectos y tareas.
- Dashboard con total de proyectos, conteo de tareas por estado, y proyectos/tareas más recientes.
- Panel de administración personalizado, con búsqueda y filtros por estado, prioridad y propietario.
- Páginas de error 404 y 500 con el mismo sistema visual del resto de la app.
- Interfaz responsiva sobre Bootstrap 5, con estilo visual propio (gradientes, tarjetas glass, badges de color).

## 🧠 Decisiones técnicas

**`settings.AUTH_USER_MODEL` en vez de importar `User` directo.** Es la práctica recomendada por Django para mantener flexibilidad ante un futuro modelo de usuario personalizado, aunque en este proyecto no se llegó a necesitar.

**`TextChoices` para estado y prioridad.** En vez de tuplas sueltas, se usó `models.TextChoices` en `Tarea`, lo que da `get_estado_display()` / `get_prioridad_display()` gratis y hace el código más legible y mantenible.

**`related_name` en todas las relaciones.** Permite escribir `usuario.proyectos.all()` o `proyecto.tareas.all()` en vez de queries más largas con `filter()`, tanto en las vistas como en los tests.

**Bootstrap + hoja de estilos propia, en vez de un framework de componentes.** Se priorizó no agregar una capa de build (Webpack, npm) para mantener el proyecto simple de instalar y correr, personalizando visualmente por encima de Bootstrap con CSS propio.

**`django-widget-tweaks` para los formularios.** Los formularios de Django no traen clases de Bootstrap por defecto; esta librería permite inyectárselas campo por campo sin tener que reescribir los widgets a mano.

**`SECRET_KEY` en variable de entorno.** Se movió fuera del código fuente con `python-dotenv`, para no exponerla al subir el proyecto a un repositorio público.

**Dashboard como pantalla de inicio tras el login.** En vez de llevar directo al listado de proyectos, se agregó una vista de resumen para dar contexto inmediato de la actividad del usuario.

## 🏗️ Construcción

Resumen del proceso de armado del proyecto, paso a paso:

1. **Estructura del proyecto.** Se creó el proyecto Django (`core`) y la app principal (`gestion`), con SQLite como base de datos por defecto.
2. **Modelos.** Se diseñaron `Proyecto` y `Tarea`, con sus relaciones (`ForeignKey`, `related_name`) y campos de estado/prioridad mediante `TextChoices`.
3. **Autenticación.** Se implementó registro (`UserCreationForm`) y se conectaron las vistas de login/logout incluidas en Django, configurando `LOGIN_URL` y las redirecciones correspondientes.
4. **Restricciones de acceso.** Se protegieron las vistas de `Proyecto` y `Tarea` con `LoginRequiredMixin`, filtrando cada consulta por el usuario autenticado para garantizar el aislamiento de datos.
5. **Formularios y CRUD.** Se construyeron las vistas de creación, edición y eliminación con `CreateView`/`UpdateView`/`DeleteView`, incluyendo la asignación automática del propietario.
6. **Panel de administración.** Se personalizó `admin.py` con columnas, búsqueda y filtros para `Proyecto` y `Tarea`.
7. **Templates.** Se armó `base.html` con herencia de plantillas, y los templates de cada vista sobre Bootstrap 5.
8. **Seguridad.** Se revisó CSRF, aislamiento de datos, `SECRET_KEY` en variable de entorno y `.gitignore`.
9. **Pruebas unitarias.** Se escribieron 12 tests cubriendo modelos, seguridad de acceso y aislamiento entre usuarios.
10. **Mejoras de diseño.** Se incorporó un dashboard, paginación, páginas de error personalizadas y un sistema visual propio sobre Bootstrap.
11. **Preparación para producción.** Se agregó `requirements.txt`, `gunicorn` y `whitenoise`, y `settings.py` pasó a leer `DEBUG`, `ALLOWED_HOSTS` y `DATABASE_URL` desde variables de entorno, listo para desplegar en Render.
12. **Documentación final.** Se compiló todo el proceso en este README.

## ▶️ Cómo ejecutar

```bash
git clone <url-del-repositorio>
cd Proy_django_gestion_tareas

python -m venv venv
venv\Scripts\activate        # En Windows
# source venv/bin/activate   # En macOS/Linux

pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz con:

```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
```

Aplicar migraciones, crear un superusuario y levantar el servidor:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir en el navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**Uso rápido:** `/registro/` para crear una cuenta → `/login/` → redirige a `/dashboard/` → gestionar proyectos en `/proyectos/` y tareas en `/tareas/`. El panel de administración está en `/admin/` (requiere superusuario).

## 🔒 Seguridad

- Protección CSRF en todos los formularios (`{% csrf_token %}`).
- Acceso restringido mediante `LoginRequiredMixin` en todas las vistas de proyectos, tareas y dashboard.
- Aislamiento de datos por usuario en cada `get_queryset()`.
- `SECRET_KEY` gestionada por variable de entorno, fuera del control de versiones.
- Validadores de contraseña por defecto de Django (`AUTH_PASSWORD_VALIDATORS`) activos.
- Páginas de error personalizadas (404/500), visibles cuando `DEBUG=False` (producción).
- `DEBUG`, `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` se controlan por variable de entorno; en producción `DEBUG` queda en `False` por defecto (no hace falta declararlo).

## 🧪 Pruebas unitarias

12 pruebas cubriendo modelos y vistas:

- Creación y representación (`__str__`) de `Proyecto` y `Tarea`.
- Valores por defecto de `estado` y `prioridad`.
- Relación entre `Proyecto` y sus `Tarea` asociadas.
- Redirección al login sin sesión iniciada.
- Aislamiento de datos entre usuarios (proyectos y tareas).
- Asignación automática del propietario al crear un proyecto.
- Filtrado correcto del campo "proyecto" en el formulario de tareas.

```bash
python manage.py test
```

## 🚀 Despliegue en Render

El proyecto está listo para desplegarse en [Render](https://render.com) (plan gratuito):

1. Crear una cuenta en Render y conectarla con GitHub.
2. **New +** → **Blueprint**, elegir este repositorio (Render detecta `render.yaml` y preconfigura todo), o **New +** → **Web Service** y completar a mano:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn core.wsgi:application`
3. Variables de entorno a definir en Render (el Blueprint ya las deja armadas):
   - `SECRET_KEY`: generarla nueva, distinta a la de desarrollo.
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: el dominio que asigna Render (ej. `gestion-tareas.onrender.com`)
   - `CSRF_TRUSTED_ORIGINS`: `https://` + ese mismo dominio
4. Con SQLite (por defecto) los datos se pierden cada vez que la instancia gratuita se reinicia por inactividad. Para persistencia real, crear una base Postgres (en Render o en [Neon](https://neon.tech), gratis) y agregar la variable `DATABASE_URL` — `settings.py` la detecta sola, sin tocar código.

> ⚠️ No se recomienda Vercel para este proyecto: es una plataforma serverless sin filesystem persistente, y esta app usa SQLite además de escrituras normales a base de datos (crear/editar proyectos y tareas), algo que no funciona de forma confiable en ese modelo.
