# Gestión de Proyectos y Tareas – Django Web App

Aplicación web desarrollada en Django que permite a los usuarios registrarse, autenticarse, y gestionar sus propios proyectos y tareas de forma segura y aislada entre usuarios.

Proyecto final del Módulo 6 (Construir aplicaciones web empresariales utilizando el patrón MVC en el entorno de desarrollo Python/Django) del bootcamp Full Stack Python Trainee (Talento Digital / Alkemy).

> Este documento describe el estado **actualmente implementado** del proyecto. Las mejoras de diseño en curso se documentan por separado en [MEJORAS_DISENO.md](MEJORAS_DISENO.md) para poder comparar el antes y el después.

## Índice

- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración de variables de entorno](#configuración-de-variables-de-entorno)
- [Uso de la aplicación](#uso-de-la-aplicación)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Pruebas unitarias](#pruebas-unitarias)
- [Seguridad](#seguridad)
- [Decisiones de diseño](#decisiones-de-diseño)

## Arquitectura del proyecto

La aplicación sigue el patrón MVC (Modelo-Vista-Controlador) propio de Django, organizada en un proyecto principal (`core`) y una app (`gestion`) que concentra toda la lógica de negocio.

### Modelos

**Proyecto**
- `nombre`: nombre del proyecto (obligatorio).
- `descripcion`: descripción del proyecto (opcional).
- `propietario`: relación `ForeignKey` con el usuario dueño del proyecto (`settings.AUTH_USER_MODEL`).
- `creado_en`: fecha de creación, se guarda automáticamente.

**Tarea**
- `titulo`: título de la tarea (obligatorio).
- `descripcion`: descripción de la tarea (opcional).
- `proyecto`: relación `ForeignKey` con el proyecto al que pertenece.
- `estado`: uno de `Pendiente`, `En progreso` o `Completada` (usando `TextChoices`).
- `prioridad`: una de `Baja`, `Media` o `Alta` (usando `TextChoices`).
- `creado_en`: fecha de creación, se guarda automáticamente.

**Relaciones:**
- Un usuario puede tener múltiples proyectos (1:N).
- Un proyecto puede tener múltiples tareas (1:N).
- Si se elimina un proyecto, se eliminan en cascada sus tareas asociadas (`on_delete=models.CASCADE`).

### Vistas

Las vistas de `Proyecto` y `Tarea` están implementadas como vistas basadas en clases (`ListView`, `CreateView`, `UpdateView`, `DeleteView`), todas protegidas con `LoginRequiredMixin`. Cada vista filtra los datos según el usuario autenticado, garantizando que un usuario nunca pueda ver, editar o eliminar información de otro usuario.

### Autenticación

El registro de usuarios se maneja con una vista propia basada en `UserCreationForm`, mientras que el login y logout utilizan las vistas incluidas en `django.contrib.auth`.

## Requisitos previos

- Python 3.10 o superior
- pip

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd Proy_django_gestion_tareas
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install django python-dotenv django-widget-tweaks
```

4. Aplicar las migraciones:

```bash
python manage.py migrate
```

5. Crear un superusuario (para acceder al panel de administración):

```bash
python manage.py createsuperuser
```

6. Levantar el servidor de desarrollo:

```bash
python manage.py runserver
```

7. Abrir en el navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Configuración de variables de entorno

El proyecto utiliza un archivo `.env` en la raíz para mantener la `SECRET_KEY` fuera del código fuente. Crear un archivo `.env` con el siguiente contenido:

```
SECRET_KEY=tu-clave-secreta-aqui
```

> El archivo `.env` no se sube al repositorio (está excluido en `.gitignore`). Cada persona que clone el proyecto debe generar su propia clave o solicitarla al autor.

## Uso de la aplicación

1. **Registro:** ingresar a `/registro/` y crear una cuenta nueva.
2. **Login:** ingresar a `/login/` con las credenciales creadas.
3. **Proyectos:** en `/proyectos/`, crear, editar o eliminar proyectos propios.
4. **Tareas:** en `/tareas/`, crear tareas asociadas a un proyecto propio, definiendo estado y prioridad.
5. **Panel de administración:** en `/admin/`, accesible solo con un superusuario, permite gestionar todos los proyectos y tareas del sistema.
6. **Logout:** disponible desde el botón "Cerrar sesión" en la barra de navegación.

## Estructura de carpetas

```
Proy_django_gestion_tareas/
├── core/                       # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── gestion/                    # App principal con la lógica de negocio
│   ├── migrations/
│   ├── templates/
│   │   └── gestion/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── registro.html
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
└── README.md
```

## Pruebas unitarias

El proyecto incluye pruebas unitarias que cubren modelos y vistas:

- Creación y representación (`__str__`) de `Proyecto` y `Tarea`.
- Valores por defecto de `estado` y `prioridad` en `Tarea`.
- Relación entre `Proyecto` y sus `Tarea` asociadas.
- Redirección al login cuando no hay sesión iniciada.
- Aislamiento de datos: un usuario no puede ver ni editar proyectos o tareas de otro usuario.
- Asignación automática del propietario al crear un proyecto.
- Filtrado correcto del campo "proyecto" en el formulario de creación de tareas.

Para ejecutar las pruebas:

```bash
python manage.py test
```

## Seguridad

- Protección CSRF en todos los formularios (`{% csrf_token %}`).
- Acceso restringido a vistas de proyectos y tareas mediante `LoginRequiredMixin`.
- Aislamiento de datos por usuario en todas las consultas (`get_queryset()`).
- `SECRET_KEY` gestionada mediante variable de entorno, fuera del control de versiones.
- Validadores de contraseña por defecto de Django (`AUTH_PASSWORD_VALIDATORS`) activos.

> Nota: `DEBUG = True` se mantiene durante el desarrollo para facilitar la depuración de errores. En un entorno de producción real, debe cambiarse a `DEBUG = False`.

## Decisiones de diseño

- Se utilizó `settings.AUTH_USER_MODEL` en lugar de importar `User` directamente, siguiendo la práctica recomendada por Django para mantener flexibilidad ante un futuro modelo de usuario personalizado.
- Se incorporaron estados (`Pendiente`, `En progreso`, `Completada`) y niveles de prioridad (`Baja`, `Media`, `Alta`) en el modelo `Tarea` mediante `TextChoices`, para reflejar un flujo de trabajo más realista.
- La interfaz se construyó con Bootstrap 5 vía CDN, sin hojas de estilo propias ni archivos estáticos adicionales: navbar oscura, tarjetas para proyectos, tabla para tareas y formularios con `django-widget-tweaks` para aplicar clases de Bootstrap a los campos generados automáticamente por Django.
- Se usó `django-widget-tweaks` para aplicar estilos de Bootstrap a los campos de formulario generados automáticamente por Django.
