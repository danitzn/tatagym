# Create your views here.

from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import PersonaForm, RegistromarcacionForm
from .models import Marcacion, Persona, PlanPersona, dashboard
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView , DetailView
from django.utils import timezone


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

#------------------planes------------------#

class ListarPlanesView(DetailView):
    model = PlanPersona
    template_name = 'estadocuenta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personas'] = Persona.objects.all()
        return context
##marcaciones


class ListarMarcacionesView(ListView):
    model = Marcacion
    template_name = 'marcaciones.html'
    context_object_name = 'marcaciones'
    ordering = ['-fecha']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()

        # Imprimir los datos de las personas
        for marcacion in queryset:
            print(marcacion)
        return queryset


from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegistromarcacionForm
from .models import Persona, PlanPersona, Marcacion

from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegistromarcacionForm
from .models import Persona, PlanPersona, Marcacion

from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegistromarcacionForm
from .models import Persona, PlanPersona, Marcacion

def registrar_marcacion(request):
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
            mensaje = 'Plan inactivo - No se puede realizar la marcación'
    else:
        mensaje = 'Error en el formulario'

    return render(request, 'marcacion.html', {'mensaje': mensaje})


def estado_cuenta (request):
    return render(request, 'estadocuenta.html')

def cargar_pago(request):
    return render(request, 'cargarpago.html')