from django import forms

from .models import Plato


class PlatoForm(forms.ModelForm):
    """Formulario base de la carta. Lo usan tanto el alta como la edición."""

    class Meta:
        model = Plato
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'stock',
            'tiempo_preparacion',
            'disponible',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lomo a lo pobre',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Lomo de vacuno con papas fritas, cebolla y dos huevos fritos.',
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 9990',
            }),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 180,
            }),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        # --- Jairo Castillo: rama jairo/mysql-validaciones ---------------------
        # Mensajes claros y en español para cada campo, en vez de los genéricos
        # de Django. 'min_value' cubre los números negativos: el campo
        # PositiveIntegerField los rechaza antes de llegar a la base de datos.
        error_messages = {
            'nombre': {
                'required': 'El nombre del plato es obligatorio y no puede quedar en blanco.',
                'max_length': 'El nombre no puede superar los 100 caracteres.',
            },
            'descripcion': {
                'required': 'La descripción es obligatoria.',
                'max_length': 'La descripción no puede superar los 300 caracteres.',
            },
            'categoria': {
                'required': 'Debes elegir una categoría.',
                'invalid_choice': 'La categoría seleccionada no es válida.',
            },
            'precio': {
                'required': 'El precio es obligatorio.',
                'invalid': 'El precio debe ser un número entero, sin puntos ni decimales.',
                'min_value': 'El precio debe ser mayor que cero; no se aceptan valores negativos.',
                'max_value': 'El precio no puede superar los $500.000.',
            },
            'stock': {
                'required': 'Indica las porciones disponibles (puede ser 0).',
                'invalid': 'Las porciones deben ser un número entero.',
                'min_value': 'Las porciones disponibles no pueden ser negativas.',
            },
            'tiempo_preparacion': {
                'required': 'El tiempo de preparación es obligatorio.',
                'invalid': 'El tiempo de preparación debe ser un número entero de minutos.',
                'min_value': 'El tiempo de preparación debe ser de al menos 1 minuto.',
                'max_value': 'El tiempo de preparación no puede superar los 180 minutos.',
            },
        }

    def clean_nombre(self):
        """Evita nombres duplicados que sólo se diferencian por mayúsculas o espacios."""
        nombre = self.cleaned_data['nombre'].strip()

        existentes = Plato.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            existentes = existentes.exclude(pk=self.instance.pk)

        if existentes.exists():
            raise forms.ValidationError('Ya existe un plato con ese nombre en la carta.')

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion'].strip()
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion
