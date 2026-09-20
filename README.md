# 🍔 El Buen Sabor — Gestión de la carta

Evaluación Sumativa 02 · Programación Backend · Temática: **Restaurante** · Entidad: **Plato**

**Integrantes**
- Jairo Alexis Castillo Carrasco — listado y alta de platos (rama `jairo/listar-crear`)
- Víctor Hugo Vergara Jara — edición y baja de platos (rama `victor/editar-eliminar`)

---

## Requisitos

- Python 3.13
- XAMPP con MariaDB 10.4 corriendo
- Django 5.0.14 (ver `requirements.txt`)

> **Importante:** este proyecto usa **Django 5.0**, no la última versión.
> Django 5.1 en adelante exige MariaDB 10.5+ y Django 6.x exige MariaDB 10.11+,
> mientras que XAMPP trae MariaDB 10.4.32. Con Django 6 la conexión falla.

## Puesta en marcha

```bash
# 1. Entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Dependencias
pip install -r requirements.txt

# 3. Levantar MySQL desde el panel de XAMPP y crear la base
mysql -u root -e "CREATE DATABASE restaurante_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 4. Crear las tablas
python manage.py migrate

# 5. Cargar platos de ejemplo (opcional)
python manage.py cargar_carta

# 6. Correr el servidor
python manage.py runserver
```

Abrir <http://localhost:8000>.

## Conexión a la base de datos

Configurada en `restaurante/settings.py`:

| Parámetro | Valor |
|---|---|
| ENGINE | `django.db.backends.mysql` |
| NAME | `restaurante_db` |
| USER | `root` |
| PASSWORD | *(vacía, por defecto en XAMPP)* |
| HOST / PORT | `127.0.0.1` / `3306` |

## Rutas

| URL | Vista | Operación |
|---|---|---|
| `/` | `inicio` | Página principal |
| `/platos/` | `lista_platos` | **R** — Consultar |
| `/platos/nuevo/` | `crear_plato` | **C** — Crear |
| `/platos/<id>/editar/` | `editar_plato` | **U** — Modificar |
| `/platos/<id>/eliminar/` | `eliminar_plato` | **D** — Eliminar |

## Validaciones del modelo `Plato`

- `nombre`: obligatorio, único (sin distinguir mayúsculas), mínimo 3 caracteres, no puede ser sólo números
- `descripcion`: obligatoria, mínimo 10 y máximo 300 caracteres
- `precio`: entero **mayor que cero**, tope $500.000
- `stock`: entero **no negativo** (`int unsigned` también a nivel de base de datos)
- `tiempo_preparacion`: entre 1 y 180 minutos
- Coherencia: un plato marcado como *disponible* no puede tener 0 porciones
