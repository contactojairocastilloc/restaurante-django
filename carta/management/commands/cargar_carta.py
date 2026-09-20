from django.core.management.base import BaseCommand

from carta.models import Plato


class Command(BaseCommand):
    help = 'Carga una carta de ejemplo para poder demostrar la aplicación.'

    PLATOS = [
        ('Empanada de pino', 'Empanada horneada rellena con carne, cebolla, huevo y aceituna.',
         Plato.ENTRADA, 2500, 40, 15),
        ('Machas a la parmesana', 'Machas gratinadas con queso parmesano y vino blanco.',
         Plato.ENTRADA, 8900, 12, 20),
        ('Lomo a lo pobre', 'Lomo de vacuno con papas fritas, cebolla caramelizada y dos huevos.',
         Plato.FONDO, 9990, 15, 25),
        ('Cazuela de vacuno', 'Caldo de vacuno con zapallo, choclo, papa y arroz.',
         Plato.FONDO, 7500, 20, 45),
        ('Congrio frito', 'Filete de congrio frito acompañado de ensalada chilena.',
         Plato.FONDO, 11900, 8, 30),
        ('Pastel de choclo', 'Choclo molido sobre pino de carne y pollo, gratinado al horno.',
         Plato.FONDO, 8500, 10, 40),
        ('Mote con huesillo', 'Duraznos deshidratados en almíbar con mote de trigo.',
         Plato.POSTRE, 2900, 25, 5),
        ('Leche asada', 'Postre horneado de leche, huevo y caramelo.',
         Plato.POSTRE, 3200, 18, 10),
        ('Jugo natural de frambuesa', 'Jugo preparado con frambuesas frescas.',
         Plato.BEBIDA, 2200, 30, 5),
        ('Pisco sour', 'Pisco, jugo de limón de Pica y azúcar flor.',
         Plato.BEBIDA, 4500, 50, 8),
    ]

    def handle(self, *args, **options):
        creados = 0

        for nombre, descripcion, categoria, precio, stock, minutos in self.PLATOS:
            plato, nuevo = Plato.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'categoria': categoria,
                    'precio': precio,
                    'stock': stock,
                    'tiempo_preparacion': minutos,
                    'disponible': True,
                },
            )
            if nuevo:
                creados += 1
                self.stdout.write(f'  + {plato.nombre}')

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {creados} plato(s) nuevo(s). Total en la carta: {Plato.objects.count()}.'
        ))
