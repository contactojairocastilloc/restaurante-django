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
    # 1. Buscamos el plato por su ID (Primary Key) o lanzamos un error 404 si no existe
    plato = get_object_or_404(Plato, pk=pk)
    
    # 2. Si el usuario envía el formulario (POST)
    if request.method == 'POST':
        # Pasamos los datos recibidos y le indicamos que actualice la 'instancia' existente
        form = PlatoForm(request.POST, instance=plato)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'El plato fue editado correctamente.')
            return redirect('carta:lista')
        else:
            messages.error(request, 'Hubo un error al editar el plato. Revisa los datos.')
            
    # 3. Si el usuario solo está entrando a la página para ver el formulario (GET)
    else:
        # Cargamos el formulario con los datos actuales del plato
        form = PlatoForm(instance=plato)
        
    # 4. Renderizamos la plantilla HTML enviando el formulario y el plato
    return render(request, 'carta/editar.html', {
        'form': form,
        'plato': plato
    })


def eliminar_plato(request, pk):
    # 1. Buscamos el plato por su ID
    plato = get_object_or_404(Plato, pk=pk)
    
    # 2. Si el usuario confirmó la eliminación presionando el botón "Sí, eliminar" (POST)
    if request.method == 'POST':
        # Borramos el plato de la base de datos
        plato.delete()
        messages.success(request, 'El plato fue eliminado exitosamente.')
        # Redirigimos al listado
        return redirect('carta:lista')
        
    # 3. Si el usuario hizo clic en el enlace "Eliminar" (GET)
    # Mostramos la pantalla de confirmación antes de borrar algo
    return render(request, 'carta/confirmar_eliminar.html', {
        'plato': plato
    })