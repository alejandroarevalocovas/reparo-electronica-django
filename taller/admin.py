from django.contrib import admin

from .models import Cliente, Pedido


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "contacto", "categoria", "localizacion"]
    search_fields = ["nombre", "contacto"]
    list_filter = ["categoria"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "equipo", "cliente", "estado", "fecha_entrada", "precio"]
    list_filter = ["estado", "garantia", "fecha_entrada"]
    search_fields = ["equipo", "numero_serie", "cliente__nombre"]
    autocomplete_fields = ["cliente"]
    date_hierarchy = "fecha_entrada"