from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import PlatoForm
from .models import Plato


# --- Jairo Castillo: rama jairo/mysql-validaciones ---------------------------
DATOS_VALIDOS = {
    'nombre': 'Lomo a lo pobre',
    'descripcion': 'Lomo de vacuno con papas fritas y huevo.',
    'categoria': Plato.FONDO,
    'precio': 9990,
    'stock': 5,
    'tiempo_preparacion': 25,
    'disponible': True,
}


class ValidacionesPlatoFormTest(TestCase):
    """El formulario no debe aceptar datos inválidos y debe explicar el error."""

    def formulario_con(self, **cambios):
        return PlatoForm(data={**DATOS_VALIDOS, **cambios})

    def test_datos_validos(self):
        self.assertTrue(self.formulario_con().is_valid())

    def test_precio_negativo(self):
        form = self.formulario_con(precio=-500)
        self.assertFalse(form.is_valid())
        self.assertIn('no se aceptan valores negativos', form.errors['precio'][0])

    def test_precio_cero(self):
        form = self.formulario_con(precio=0)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_precio_con_decimales(self):
        form = self.formulario_con(precio='99.5')
        self.assertFalse(form.is_valid())
        self.assertIn('número entero', form.errors['precio'][0])

    def test_nombre_en_blanco(self):
        for nombre in ('', '     '):
            form = self.formulario_con(nombre=nombre)
            self.assertFalse(form.is_valid())
            self.assertIn('no puede quedar en blanco', form.errors['nombre'][0])

    def test_nombre_solo_numeros(self):
        form = self.formulario_con(nombre='12345')
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_nombre_duplicado_sin_importar_mayusculas(self):
        Plato.objects.create(**DATOS_VALIDOS)
        form = self.formulario_con(nombre='LOMO A LO POBRE')
        self.assertFalse(form.is_valid())
        self.assertIn('Ya existe', form.errors['nombre'][0])

    def test_stock_negativo(self):
        form = self.formulario_con(stock=-1)
        self.assertFalse(form.is_valid())
        self.assertIn('no pueden ser negativas', form.errors['stock'][0])

    def test_disponible_sin_stock(self):
        form = self.formulario_con(stock=0, disponible=True)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)


class CrudPersistenciaTest(TestCase):
    """El CRUD guarda lo válido en la base de datos y rechaza lo inválido."""

    def setUp(self):
        User.objects.create_user('mesero', password='clave-de-prueba-123')
        self.client.login(username='mesero', password='clave-de-prueba-123')

    def test_crear_plato_valido_se_guarda(self):
        respuesta = self.client.post(reverse('carta:crear'), DATOS_VALIDOS)
        self.assertRedirects(respuesta, reverse('carta:lista'))
        self.assertTrue(Plato.objects.filter(nombre='Lomo a lo pobre').exists())

    def test_crear_plato_invalido_no_se_guarda(self):
        datos = {**DATOS_VALIDOS, 'nombre': '', 'precio': -100}
        respuesta = self.client.post(reverse('carta:crear'), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'no puede quedar en blanco')
        self.assertContains(respuesta, 'no se aceptan valores negativos')
        self.assertEqual(Plato.objects.count(), 0)

    def test_editar_con_precio_negativo_no_modifica(self):
        plato = Plato.objects.create(**DATOS_VALIDOS)
        datos = {**DATOS_VALIDOS, 'precio': -1}
        respuesta = self.client.post(reverse('carta:editar', args=[plato.pk]), datos)
        self.assertContains(respuesta, 'no se aceptan valores negativos')
        plato.refresh_from_db()
        self.assertEqual(plato.precio, 9990)
