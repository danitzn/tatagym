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
def registrar_marcacion(request):
    cedula = request.POST.get('cedula')
    try:
        persona = Persona.objects.get(cedula=cedula)
        plan_persona = PlanPersona.objects.get(persona=persona)

        if plan_persona.estado == 'activo':
            marcaciones = Marcacion.objects.filter(persona_plan__persona=persona, fecha__date=timezone.now().date())

            if marcaciones.exists():
                ultimo_tipo_marcacion = marcaciones.latest('fecha').tipo
                tipo_marcacion = 'entrada' if ultimo_tipo_marcacion == 'salida' else 'salida'
            else:
                tipo_marcacion = 'entrada'

            marcacion = Marcacion()
            marcacion.fecha = timezone.now()
            marcacion.cedula = cedula
            marcacion.tipo = tipo_marcacion
            marcacion.plan_persona = plan_persona
            marcacion.save()

            mensaje = 'Marcación exitosa - Tipo: {}'.format(tipo_marcacion)
        else:
            mensaje = 'Plan inactivo - No se puede realizar la marcación'
    except Persona.DoesNotExist:
        mensaje = 'No está registrado en el sistema'

    return render(request, 'marcacion.html', {'mensaje': mensaje})


def estado_cuenta (request):
    return render(request, 'estadocuenta.html')

def cargar_pago(request):
    return render(request, 'cargarpago.html')