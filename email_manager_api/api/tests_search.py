from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Correo, Empresa
from .serializers import CorreoSerializer


class CorreoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        nueva_empresa = Empresa.objects.create(nombre="Mi nueva empresa")
        self.correo1 = Correo.objects.create(
            contenido="Hola, ¿cómo estás?",
            empresa_emisora=nueva_empresa,
            empresa_destinataria=nueva_empresa,
            fecha="2022-02-01"
        )
        self.correo2 = Correo.objects.create(
            contenido="¿Quieres reunirte mañana?",
            empresa_emisora=nueva_empresa,
            empresa_destinataria=nueva_empresa,
            fecha="2022-02-02"
        )

        self.valid_payload = {
            "contenido": "Un nuevo correo",
            "empresa_emisora": "Empresa1",
            "destinatario": "Empresa2",
            "fecha": "2022-02-03"
        }
        self.invalid_payload = {
            "contenido": "",
            "empresa_emisora": "",
            "destinatario": "",
            "fecha": ""
        }

    def test_get_all_correos(self):
        response = self.client.get(reverse("buscar_correos_api"))
        correos = Correo.objects.all()
        serializer = CorreoSerializer(correos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correo_by_contenido(self):
        response = self.client.get(reverse("buscar_correos_api") + "?contenido=Hola")
        correos = Correo.objects.filter(contenido__icontains="Hola")
        serializer = CorreoSerializer(correos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correo_by_empresa_emisora(self):
        response = self.client.get(reverse("buscar_correos_api") + "?empresa_emisora=Empresa1")
        correos = Correo.objects.filter(empresa_emisora__nombre__icontains="Empresa1")
        serializer = CorreoSerializer(correos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correo_by_empresa_destinataria(self):
        response = self.client.get(reverse("buscar_correos_api") + "?empresa_destinataria=Empresa2")
        correos = Correo.objects.filter(empresa_destinataria__nombre__icontains="Empresa2")
        serializer = CorreoSerializer(correos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correo_by_fecha(self):
        response = self.client.get(reverse("buscar_correos_api") + "?fecha_desde=2022-02-01&fecha_hasta=2022-02-02")
        correos = Correo.objects.filter(fecha__range=["2022-02-01", "2022-02-02"])
        serializer = CorreoSerializer(correos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
