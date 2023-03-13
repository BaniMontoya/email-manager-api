from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
import json

from .models import Correo, Empresa


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class RegistraCorreoAPIViewTest(TestCase):
   def setUp(self):
    self.client = Client()
    self.empresa = Empresa.objects.create(nombre='Google')
    self.email_empresa1 = 'empresa1@domain.com'
    self.email_empresa2 = 'empresa2@domain.com'
    self.content_type = 'application/json'
    self.valid_payload = {
        'destinatario': self.email_empresa1,
        'emisor': self.email_empresa2,
        'fecha': datetime.now(),
        'empresa_emisora': self.empresa.id,
        'codigo_proveedor': 'ABC123'
    }
    self.invalid_payload = {
        'destinatario': '',
        'emisor': self.email_empresa1,
        'fecha': datetime.now(),
        'empresa_emisora': self.empresa.id,
        'codigo_proveedor': 'ABC123'
    }


    def test_create_valid_correo(self):
        response = self.client.post(
            reverse('registra-correo'),
            data=json.dumps(self.valid_payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_correo(self):
        response = self.client.post(
            reverse('registra-correo'),
            data=json.dumps(self.invalid_payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 400)

    def test_create_correo_with_unknown_empresa(self):
        payload = {
            'destinatario': self.email_empresa1,
            'emisor': self.email_empresa2,
            'fecha': datetime.now(),
            'empresa_emisora': 'Unknown Company',
            'codigo_proveedor': 'ABC123'
        }
        response = self.client.post(
            reverse('registra-correo'),
            data=json.dumps(payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 400)

    def test_create_correo_without_empresa(self):
        payload = {
            'destinatario': self.email_empresa1,
            'emisor': self.email_empresa2,
            'fecha': datetime.now(),
            'codigo_proveedor': 'ABC123'
        }
        response = self.client.post(
            reverse('registra-correo'),
            data=json.dumps(payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 400)

    def test_update_valid_correo(self):
        correo = Correo.objects.create(
            destinatario=self.email_empresa1,
            emisor=self.email_empresa2,
            fecha=datetime.now(),
            empresa_emisora=self.empresa,
            codigo_proveedor='ABC123'
        )
        payload = {
            'destinatario': self.email_empresa1,
            'emisor': self.email_empresa2,
            'fecha': datetime.now(),
            'empresa_emisora': self.empresa.id,
            'codigo_proveedor': 'XYZ456'
        }
        response = self.client.put(
            reverse('actualiza-correo', kwargs={'pk': correo.pk}),
            data=json.dumps(payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 200)
        correo.refresh_from_db()
        self.assertEqual(correo.codigo_proveedor, 'XYZ456')

    def test_update_invalid_correo(self):
        correo = Correo.objects.create(
            destinatario=self.email_empresa1,
            emisor='jane@example.com',
            fecha=datetime.now(),
            empresa_emisora=self.empresa,
            codigo_proveedor='ABC123'
        )
        payload = {
            'destinatario': '',
            'emisor': 'jane@example.com',
            'fecha': datetime.now(),
            'empresa_emisora': self.empresa.id,
            'codigo_proveedor': 'XYZ456'
        }
        response = self.client.put(
            reverse('actualiza-correo', kwargs={'pk': correo.pk}),
            data=json.dumps(payload, cls=DateTimeEncoder),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, 400)
        correo.refresh_from_db()
        self.assertEqual(correo.codigo_proveedor, 'ABC123')


