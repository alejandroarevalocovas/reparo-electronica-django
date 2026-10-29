from django.contrib import admin

from .models import Cliente, Pedido, PedidoStock, Stock

class PedidoStockInline(admin.TabularInline):
    model = PedidoStock
    extra = 1
    autocomplete_fields = ["stock"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "contacto", "categoria", "localizacion"]
    search_fields = ["nombre", "contacto"]
    list_filter = ["categoria"]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["referencia", "tipo", "cantidad", "cantidad_total", "ubicacion", "precio"]
    list_filter = ["tipo", "estado"]
    search_fields = ["referencia", "tipo"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "equipo", "cliente", "estado", "fecha_entrada", "precio"]
    list_filter = ["estado", "garantia", "fecha_entrada"]
    search_fields = ["equipo", "numero_serie", "cliente__nombre"]
    autocomplete_fields = ["cliente"]
    date_hierarchy = "fecha_entrada"
    inlines = [PedidoStockInline]

