#forms
from django import forms
from django.forms import modelform_factory

from . models import Persona, Marcacion, PlanPersona


PersonaForm = modelform_factory(Persona, fields=('nombre', 'apellido', 'edad', 'cedula', 'telefono', 'correo'))

class RegistromarcacionForm(forms.ModelForm):
    cedula = forms.CharField(widget=forms.HiddenInput())
    estado_plan = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # Resto del código del formulario

    class Meta:
        model = Marcacion
        fields = ['cedula', 'estado_plan']

class PersonaPlanForm(forms.ModelForm):
     id = forms.IntegerField(widget=forms.HiddenInput())
     id_persona = forms.CharField(widget=forms.HiddenInput())
     id_plan = forms.CharField(widget=forms.HiddenInput())
     fecha_inicio = forms.DateField(widget=forms.HiddenInput())
     fecha_fin = forms.DateField(widget=forms.HiddenInput())
     estado = forms.CharField(widget=forms.HiddenInput())