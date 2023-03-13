from django.urls import path
from .views import RegistraCorreoAPIView, BuscarCorreoAPIView

urlpatterns = [
   path('registra-correo/', RegistraCorreoAPIView.as_view(), name='registra-correo'),
   path('busca-correo/', BuscarCorreoAPIView.as_view(), name='buscar_correos_api'),
]
