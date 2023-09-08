# Create your views here.
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
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

    def post(self, request):  # Cambiar el nombre del método a 'post'
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
                mensaje = 'Plan inactivo o sin registro - No se puede realizar la marcación'
            #si la persona tiene un plan con fecha de vencimiento menor a la fecha de hoy que le salga un mensaje de regularizar estado de cuenta
            if plan_persona.fecha_fin < timezone.now().date():
                mensaje = 'Regularizar estado de Plan'

        else:
            mensaje = 'Error en el formulario'

        return render(request, 'marcacion.html', {'mensaje': mensaje})

#------------------planes------------------#
class CreatePlanPersonaView(View):
    template_name = 'registrar_plan.html'

    def get(self, request):
        planpersona_form = PlanPersonaForm()
        return render(request, self.template_name, {'planpersona_form': planpersona_form})

    def post(self, request):
        planpersona_form = PlanPersonaForm(request.POST)
        if planpersona_form.is_valid():
            planpersona_form.save()
            return redirect('dashboard')  # Asegúrate de que 'dashboard' sea la URL correcta a la que deseas redirigir
        else:
            # Si el formulario no es válido, puedes manejarlo de alguna manera, como mostrar un mensaje de error
            error_message = "Hubo un error en el formulario, por favor verifica los datos ingresados."
            return render(request, self.template_name, {'planpersona_form': planpersona_form, 'error_message': error_message})
    
class ListarPlanesView(ListView):
    model = PlanPersona
    template_name = 'estadocuenta.html'
    context_object_name = 'planes'
    ordering = ['-fecha']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()

        # Imprimir los datos de las personas
        for plan in queryset:
            print(plan)
        return queryset

class UpdatePlanView(View):
    template_name = 'modificarplan.html'

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