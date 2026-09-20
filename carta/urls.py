from django.urls import path

from . import views

app_name = 'carta'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('platos/', views.lista_platos, name='lista'),
    path('platos/nuevo/', views.crear_plato, name='crear'),
    path('platos/<int:pk>/editar/', views.editar_plato, name='editar'),
    path('platos/<int:pk>/eliminar/', views.eliminar_plato, name='eliminar'),
]
