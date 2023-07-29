from django.contrib import admin
from django.urls import path
from gym.views import  ListarPersonasView, ListarPlanesView, dashboard, registrar_marcacion
from gym.views import registro_personas, estado_cuenta,mostrar_personas, ListarPersonasView, ListarPlanesView, ListarMarcacionesView
from gym.views import dashboard, registrar_marcacion, registro_personas, estado_cuenta, mostrar_personas

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('altapersona/', registro_personas, name='altapersona'),
    path('estadopago/', estado_cuenta, name='estadocuenta'),
    path('admin/', admin.site.urls),
    path('registrar_marcacion/', registrar_marcacion, name='registrar_marcacion'),
    path('marcaciones/', ListarMarcacionesView.as_view(), name='marcaciones'),
    path('mostrarpersona/', ListarPersonasView.as_view(), name='mostrarpersona'),
    path('personas/<int:id>/', mostrar_personas, name='personas'),
    path('estadocuenta/<int:pk>/', ListarPlanesView.as_view(), name='estadocuenta'),
    path('personas/', mostrar_personas, name='personas'),
]
