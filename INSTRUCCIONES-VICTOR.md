# Encargo para Víctor — edición y baja de platos

Hola Víctor. La base del proyecto ya está lista y funcionando contra MariaDB.
Tu parte son las operaciones **U** (modificar) y **D** (eliminar) del CRUD.

## 1. Deja tu equipo andando

```bash
git clone <URL-del-repo>
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Levanta MySQL en XAMPP y después:

```bash
mysql -u root -e "CREATE DATABASE restaurante_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
python manage.py migrate
python manage.py cargar_carta
python manage.py runserver
```

## 2. Trabaja en tu rama

```bash
git checkout victor/editar-eliminar
```

**No trabajes en `main`.** La rúbrica da 5 puntos por que cada uno tenga su
rama con sus propios commits, y la defensa individual vale 40 puntos: tienes
que poder explicar código escrito por ti.

## 3. Lo que hay que escribir

### a) `carta/views.py`

Reemplaza estas dos funciones, que hoy están como `NotImplementedError`:

```python
def editar_plato(request, pk):
    # 1. Buscar el plato con get_object_or_404(Plato, pk=pk)
    # 2. Si el método es POST: PlatoForm(request.POST, instance=plato)
    #    - si is_valid(): guardar, mensaje de éxito, redirect a 'carta:lista'
    #    - si no: mensaje de error
    # 3. Si es GET: PlatoForm(instance=plato)  -> llega con los datos cargados
    # 4. render a 'carta/editar.html' con el formulario y el plato
    ...

def eliminar_plato(request, pk):
    # 1. Buscar el plato con get_object_or_404(Plato, pk=pk)
    # 2. Si el método es POST: plato.delete(), mensaje, redirect a 'carta:lista'
    # 3. Si es GET: render a 'carta/confirmar_eliminar.html' con el plato
    #    (nunca borrar en un GET: un link no debe destruir datos)
    ...
```

Las rutas ya existen en `carta/urls.py`, no tienes que tocarlas.

### b) `templates/carta/editar.html`

⚠️ **Tiene que ser un archivo distinto de `crear.html`.** El enunciado lo pide
literalmente: *"Formulario para crear. (Deben ser distintos) / Formulario para
editar. (Deben ser distintos)"*.

Puedes guiarte por `crear.html`, pero cámbialo de verdad: título "Editar plato",
botón "Guardar cambios", muestra el nombre del plato que se está editando y
agrega un link para volver.

### c) `templates/carta/confirmar_eliminar.html`

Pantalla de confirmación antes de borrar. Debe mostrar los datos del plato y
un formulario `method="post"` con `{% csrf_token %}`, con un botón rojo
"Sí, eliminar" y otro "Cancelar" que vuelva al listado.

## 4. Commits

Haz varios commits chicos y descriptivos, no uno solo al final. Por ejemplo:

```bash
git add carta/views.py templates/carta/editar.html
git commit -m "Edición de platos (U del CRUD)"

git add templates/carta/confirmar_eliminar.html
git commit -m "Pantalla de confirmación para eliminar un plato"

git add carta/views.py
git commit -m "Baja de platos con confirmación previa (D del CRUD)"
```

Después:

```bash
git push origin victor/editar-eliminar
```

## 5. Prepárate para estas preguntas

Son del tipo que te pueden hacer en la defensa sobre tu parte:

1. ¿Por qué `get_object_or_404` y no `Plato.objects.get(pk=pk)`?
2. ¿Qué hace `instance=plato` en el `ModelForm` y qué pasaría si no lo pusieras?
3. ¿Por qué la eliminación se hace con POST y no con un simple link GET?
4. ¿Para qué sirve `{% csrf_token %}`?
5. Muestra en phpMyAdmin que el registro efectivamente desapareció de la tabla.
