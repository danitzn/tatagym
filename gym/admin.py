from django.contrib import admin
from .models import Marcacion, Persona, Plan, PlanPersona

# Register your models here.
admin.site.register(Persona)
admin.site.register(Plan)
admin.site.register(PlanPersona)
admin.site.register(Marcacion)
