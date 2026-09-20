from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.db import models


class Plato(models.Model):
    """Plato de la carta del restaurante."""

    ENTRADA = 'ENT'
    FONDO = 'FON'
    POSTRE = 'POS'
    BEBIDA = 'BEB'

    CATEGORIAS = [
        (ENTRADA, 'Entrada'),
        (FONDO, 'Plato de fondo'),
        (POSTRE, 'Postre'),
        (BEBIDA, 'Bebida'),
    ]

    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres.')],
        verbose_name='Nombre del plato',
        error_messages={'unique': 'Ya existe un plato con ese nombre en la carta.'},
    )
    descripcion = models.TextField(
        max_length=300,
        verbose_name='Descripción',
        help_text='Ingredientes principales o forma de preparación (máx. 300 caracteres).',
    )
    categoria = models.CharField(
        max_length=3,
        choices=CATEGORIAS,
        default=FONDO,
        verbose_name='Categoría',
    )
    precio = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'El precio debe ser mayor que cero.'),
            MaxValueValidator(500000, 'El precio no puede superar los $500.000.'),
        ],
        verbose_name='Precio',
        help_text='Precio en pesos chilenos, sin puntos ni decimales.',
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Porciones disponibles',
        help_text='Cantidad de porciones disponibles hoy. No puede ser negativo.',
    )
    tiempo_preparacion = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'El tiempo de preparación debe ser de al menos 1 minuto.'),
            MaxValueValidator(180, 'El tiempo de preparación no puede superar los 180 minutos.'),
        ],
        verbose_name='Tiempo de preparación',
        help_text='Minutos que demora la preparación.',
    )
    disponible = models.BooleanField(
        default=True,
        verbose_name='Disponible en carta',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última modificación')

    class Meta:
        db_table = 'carta_plato'
        ordering = ['categoria', 'nombre']
        verbose_name = 'Plato'
        verbose_name_plural = 'Platos'

    def __str__(self):
        return f'{self.nombre} (${self.precio:,})'.replace(',', '.')

    def clean(self):
        """Validaciones que dependen de más de un campo."""
        super().clean()

        # Un nombre compuesto sólo por números no es un nombre de plato válido.
        if self.nombre and self.nombre.strip().isdigit():
            raise ValidationError({'nombre': 'El nombre no puede ser sólo números.'})

        # Si no queda stock, el plato no puede seguir ofreciéndose como disponible.
        if self.disponible and self.stock == 0:
            raise ValidationError({
                'stock': 'Un plato marcado como disponible debe tener al menos 1 porción.'
            })

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip()
        super().save(*args, **kwargs)
