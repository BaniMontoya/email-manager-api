from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class Correo(models.Model):
    destinatario = models.CharField(max_length=255)
    emisor = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    empresa_emisora = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='correos_enviados', default="")
    empresa_destinataria = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='correos_recibidos', default="")
    codigo_proveedor_smtp = models.CharField(max_length=255)
    contenido = models.TextField(default="", blank=False)

    def __str__(self):
        return f'{self.emisor} -> {self.destinatario}'
