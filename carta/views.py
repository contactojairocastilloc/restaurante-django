from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PlatoForm
from .models import Plato


def inicio(request):
    """Página principal del restaurante."""
    return render(request, 'carta/inicio.html', {
        'total_platos': Plato.objects.count(),
        'destacados': Plato.objects.filter(disponible=True)[:3],
    })


# --- Jairo Castillo: rama jairo/listar-crear ---------------------------------

def lista_platos(request):
    """R del CRUD: consulta los platos guardados en MySQL/MariaDB."""
    platos = Plato.objects.all()

    # Filtro por texto: busca en el nombre o en la descripción.
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        platos = platos.filter(nombre__icontains=busqueda) | platos.filter(
            descripcion__icontains=busqueda
        )

    # Filtro por categoría.
    categoria = request.GET.get('categoria', '')
    if categoria:
        platos = platos.filter(categoria=categoria)

    return render(request, 'carta/lista.html', {
        'platos': platos,
        'busqueda': busqueda,
        'categoria_activa': categoria,
        'categorias': Plato.CATEGORIAS,
    })


def crear_plato(request):
    """C del CRUD: inserta un plato nuevo en MySQL/MariaDB."""
    if request.method == 'POST':
        formulario = PlatoForm(request.POST)
        if formulario.is_valid():
            plato = formulario.save()
            messages.success(
                request,
                f'El plato "{plato.nombre}" se agregó correctamente a la carta.',
            )
            return redirect('carta:lista')
        messages.error(request, 'Revisa los datos: el formulario tiene errores.')
    else:
        formulario = PlatoForm()

    return render(request, 'carta/crear.html', {'formulario': formulario})


# --- Víctor Vergara: rama victor/editar-eliminar -----------------------------

def editar_plato(request, pk):
    raise NotImplementedError('TODO Víctor: edición de un plato (U del CRUD).')


def eliminar_plato(request, pk):
    raise NotImplementedError('TODO Víctor: baja de un plato (D del CRUD).')
