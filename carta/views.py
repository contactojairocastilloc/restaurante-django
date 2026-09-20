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
    raise NotImplementedError('TODO Jairo: listado de platos (R del CRUD).')


def crear_plato(request):
    raise NotImplementedError('TODO Jairo: alta de un plato (C del CRUD).')


# --- Víctor Vergara: rama victor/editar-eliminar -----------------------------

def editar_plato(request, pk):
    raise NotImplementedError('TODO Víctor: edición de un plato (U del CRUD).')


def eliminar_plato(request, pk):
    raise NotImplementedError('TODO Víctor: baja de un plato (D del CRUD).')
