from rest_framework import serializers
from .models import Correo, Empresa

class CorreoSerializer(serializers.Serializer):
    destinatario = serializers.CharField(max_length=255)
    emisor = serializers.CharField(max_length=255)
    fecha = serializers.DateTimeField()
    empresa_emisora = serializers.CharField(max_length=255)
    codigo_proveedor_smtp = serializers.CharField(max_length=255)

    def validate_empresa_emisora(self, value):
        """
        Validamos que la empresa emisora del correo esté en nuestro catálogo de empresas conocidas.
        """
        try:
            empresa = Empresa.objects.get(nombre=value)
        except Empresa.DoesNotExist:
            raise serializers.ValidationError('La empresa emisora del correo no está en nuestro catálogo de empresas conocidas')
        return value

    def create(self, validated_data):
        """
        Creamos y devolvemos una nueva instancia de Correo, utilizando los datos validados.
        """
        return Correo.objects.create(**validated_data)
