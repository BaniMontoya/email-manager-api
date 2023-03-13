from django.contrib import admin
from .models import Empresa, Correo

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Correo)
class CorreoAdmin(admin.ModelAdmin):
    list_display = ('destinatario', 'emisor', 'fecha', 'empresa_emisora', 'codigo_proveedor_smtp')
