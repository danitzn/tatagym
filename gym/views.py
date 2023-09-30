# Create your views here.
from datetime import date, timedelta
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from sklearn import logger
from .forms import PersonaForm, RegistromarcacionForm, PlanPersonaForm
from .models import Marcacion, Persona, PlanPersona,Estados, dashboard
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView , DetailView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView



#forms persona

class PersonaView(View):
    template_name = 'altapersona.html'

    def get(self, request):
        form = PersonaForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Cambia 'altapersona' por 'dashboard' si esa es la vista a la que deseas redirigir después de guardar los datos
        return render(request, self.template_name, {'form': form})
    
from django.views.generic import ListView

class ListarPersonasView(ListView):
    model = Persona
    template_name = 'dashboard.html'
    context_object_name = 'personas'
    ordering = ['-fecha']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()

        # Imprimir los datos de las personas
        for persona in queryset:
            print(persona)
        return queryset
    
def registro_personas(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Cambia 'altapersona' por 'dashboard' si esa es la vista a la que deseas redirigir después de guardar los datos
    else:
        form = PersonaForm()
    return render(request, 'altapersona.html', {'form': form})

def mostrar_personas(request):
    #personas = Persona.objects.all()[:5]#
    personas = Persona.objects.order_by('-fecha')[:5]
    return render(request, 'personas.html', {'personas': personas})
def contar_personas(request):
    personas = Persona.objects.all()
    return render(request, 'dashboard.html', {'personas': personas})

#------------------marcaciones------------------#
class MarcacionView(View):
    template_name = 'marcacion.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = RegistromarcacionForm()
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = RegistromarcacionForm(request.POST)

        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            try:
                persona = Persona.objects.get(cedula=cedula)
                plan_persona = PlanPersona.objects.get(persona=persona, estado='activo')
                marcaciones_hoy = Marcacion.objects.filter(plan_persona=plan_persona, fecha__date=timezone.now().date())
                tipo_marcacion = 'entrada' if not marcaciones_hoy.exists() or marcaciones_hoy.count() % 2 == 0 else 'salida'
                marcacion = form.save(commit=False)
                marcacion.persona = persona
                marcacion.plan_persona = plan_persona
                marcacion.fecha = timezone.now()
                marcacion.tipo = tipo_marcacion
                marcacion.save()
                mensaje = f'Marcación exitosa - Tipo: {tipo_marcacion}'
            except Persona.DoesNotExist:
                mensaje = 'No está registrado en el sistema'
            except PlanPersona.DoesNotExist:
                mensaje = 'No cuenta con plan activo - No se puede realizar la marcación'
        else:
            mensaje = 'Error en el formulario'

        return render(request, self.template_name, {'mensaje': mensaje})



#------------------planes------------------#
from django.shortcuts import get_object_or_404

class CreatePlanPersonaView(View):
    template_name = 'registrar_plan.html'

    def get(self, request):
        planpersona_form = PlanPersonaForm()
        return render(request, self.template_name, {'planpersona_form': planpersona_form})

    def post(self, request):
        planpersona_form = PlanPersonaForm(request.POST)
        if planpersona_form.is_valid():
            # Obtener los datos del formulario
            data = planpersona_form.cleaned_data
            nombre = data['persona']

            # Verificar si ya existe un plan con el mismo nombre en la base de datos
            existing_plan = PlanPersona.objects.filter(persona=nombre).first()

            if existing_plan:
                # Si existe, actualiza el plan existente con los nuevos datos
                existing_plan.fecha_fin = data['fecha_fin']
                existing_plan.save()
            else:
                # Si no existe, crea un nuevo plan
                planpersona_form.save()

            return redirect('dashboard')  # Asegúrate de que 'dashboard' sea la URL correcta a la que deseas redirigir
        else:
            # Si el formulario no es válido, puedes manejarlo de alguna manera, como mostrar un mensaje de error
            error_message = "Hubo un error en el formulario, por favor verifica los datos ingresados."
            return render(request, self.template_name, {'planpersona_form': planpersona_form, 'error_message': error_message})

class PlanPersonaListView(ListView):
    model = PlanPersona
    template_name = 'estadocuenta.html'
    context_object_name = 'planes'
    ordering = ['-fecha_inicio']
    ordering = ['-fecha_fin']
    paginate_by = 30
    def get_queryset(self):
        queryset = super().get_queryset().all()
        for plan in queryset:
            print(plan)
        return queryset
    

def actualizar_cuenta(request):
    # Verificar y actualizar los estados de PlanPersona
    planes = PlanPersona.objects.all()
    for plan in planes:
        if plan.fecha_fin < date.today() and plan.estado != 'inactivo':
            plan.estado = 'inactivo'
            plan.save()
    # Obtener los planes actualizados
    planes_actualizados = PlanPersona.objects.all()

    return redirect ('estadocuenta')

class UpdatePlanView(View):
    template_name = 'modificar_plan.html'

    def get(self, request, pk):
        plan = get_object_or_404(PlanPersona, pk=pk)
        form = PlanPersonaForm(instance=plan)
        return render(request, self.template_name, {'PlanPersonaForm': form})
    
    def post(self, request, pk):
        plan = get_object_or_404(PlanPersona, pk=pk)
        form = PlanPersonaForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Cambia 'altapersona' por 'dashboard' si esa es la vista a la que deseas redirigir después de guardar los datos
        return render(request, self.template_name, {'form': form})

def http_method_not_allowed(self, request, *args, **kwargs):
    logger.warning(
        'Method Not Allowed (%s): %s', request.method, request.path,
        extra={'status_code': 405, 'request': request}
    )
    return HttpResponseNotAllowed(self._allowed_methods())
   