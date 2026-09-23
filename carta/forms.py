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
            # AQUÍ ESTÁ EL CAMBIO PARA EL PRECIO
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 9990',
                'oninvalid': "this.setCustomValidity('El valor debe ser mayor o igual a cero.')",
                'oninput': "this.setCustomValidity('')"
            }),
            # AQUÍ ESTÁ EL CAMBIO PARA EL STOCK (porciones)
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0,
                'oninvalid': "this.setCustomValidity('El valor debe ser mayor o igual a cero.')",
                'oninput': "this.setCustomValidity('')"
            }),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 180,
            }),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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