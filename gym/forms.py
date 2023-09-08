#forms
from datetime import timedelta
from django import forms
from django.forms import DateInput, modelform_factory
from . models import Estados, Persona, Marcacion, Plan, PlanPersona



PersonaForm = modelform_factory(Persona, fields=('nombre', 'apellido', 'edad', 'cedula', 'telefono', 'correo'))

class RegistromarcacionForm(forms.ModelForm):
    cedula = forms.CharField(widget=forms.HiddenInput())
    estado_plan = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Marcacion
        fields = ['cedula', 'estado_plan']

class DateInput(forms.DateInput):
    input_type = 'date'

class PlanPersonaForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=DateInput())
    fecha_fin = forms.DateField(widget=DateInput())
    estado = forms.ModelChoiceField(queryset = Estados.objects.all())
    persona = forms.ModelChoiceField(queryset=Persona.objects.all())
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())
    class Meta:
        model = PlanPersona
        fields = ['fecha_inicio', 'fecha_fin', 'estado', 'persona', 'plan']
        PlanPersonaFormset = modelform_factory(PlanPersona, fields=('fecha_inicio', 'fecha_fin', 'estado', 'persona', 'plan'))