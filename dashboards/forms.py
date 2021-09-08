# Django
from django import forms

# Models
from dashboards.models import Vehiculo, Excel

class VehiculoForm(forms.ModelForm):
    # Model form del Prelive
    class Meta:
        # Configuración del Form
        model = Vehiculo
        fields = ("numero_economico",)

class ExcelForm(forms.ModelForm):
    # Model form del Prelive
    class Meta:
        # Configuración del Form
        model = Excel
        fields = ("file",)