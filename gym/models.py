import os
from django.db import models
from django.dispatch import receiver
from django.shortcuts import render
from django.db.models.signals import post_migrate

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.precio}"

class Estados(models.Model):
    ESTADOS= (
        ('activo', 'activo'),
        ('inactivo', 'inactivo'),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS)

    def __str__(self):
        return self.estado


class PlanPersona(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=10, choices=Estados.ESTADOS)

    def __str__(self):
        return f"{self.persona} - {self.plan} - {self.fecha_inicio} - {self.fecha_fin} - {self.estado}"

    def get_plan(self):
        return self.plan.nombre

    def get_persona(self):
        return self.persona.nombre


    def __str__(self):
        return f"{self.persona} - {self.plan} - {self.fecha_inicio} - {self.fecha_fin} - {self.estado}"
    def get_plan(self):
        return self.plan.nombre
    def get_persona(self):
        return self.persona.nombre

class Marcacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cedula = models.CharField(max_length=10)
    tipo = models.CharField(max_length=10, default='entrada')
    plan_persona = models.ForeignKey(PlanPersona, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.fecha} - {self.cedula} - {self.tipo}"

def dashboard(request):
    personas = Persona.objects.all()
    marcacion = Marcacion.objects.order_by('-fecha')[:5]  # Obtén las últimas 5 marcacion

    return render(request, 'dashboard.html', {'personas': personas, 'marcacion': marcacion})

@receiver(post_migrate)
def create_estados(sender, **kwargs):
    if not os.environ.get('CREATE_INITIAL_DATA'):
        if not Estados.objects.filter(estado='activo').exists():
            Estados.objects.get_or_create(estado='activo')
        if not Estados.objects.filter(estado='inactivo').exists():
            Estados.objects.get_or_create(estado='inactivo')
        os.environ['CREATE_INITIAL_DATA'] = 'True'