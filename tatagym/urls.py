from django.contrib import admin
from django.urls import path
from gym.views import  CreatePlanPersonaView, ListarPersonasView, ListarPlanesView, MarcacionView
from gym.views import registro_personas,mostrar_personas, ListarPersonasView, ListarPlanesView
from gym.views import dashboard,registro_personas, mostrar_personas

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('altapersona/', registro_personas, name='altapersona'),
    path('dashboard/registrar_plan/',CreatePlanPersonaView.as_view(), name='registrar_plan'),
    path('admin/', admin.site.urls),
    path('registrar_marcacion/', MarcacionView.as_view(), name='registrar_marcacion'),
    path('listar_personas/', ListarPersonasView.as_view(), name='listar_personas'),
    path('personas/<int:id>/', mostrar_personas, name='personas'),
    path('estadocuenta/<int:pk>/', ListarPlanesView.as_view(), name='estadocuenta'),
]

