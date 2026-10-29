from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Cliente(models.Model):
    class Categoria(models.TextChoices):
        PARTICULAR = "particular", "Particular"
        EMPRESA = "empresa", "Empresa"
        DISTRIBUIDOR = "distribuidor", "Distribuidor"

    nombre = models.CharField(max_length=100)
    localizacion = models.CharField(max_length=100, blank=True)
    contacto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    contacta_por = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    referencia = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    formato = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)

    cantidad = models.PositiveIntegerField(null=True, blank=True)
    cantidad_total = models.PositiveIntegerField()
    cantidad_minima = models.PositiveIntegerField(null=True, blank=True)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateField(null=True, blank=True)
    enlace_compra = models.URLField(max_length=255, blank=True)
    visto_en = models.CharField(max_length=255, blank=True)
    fecha_actual = models.DateField(null=True, blank=True)

    comentarios = models.TextField(blank=True)
    detalles = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["referencia"]
        verbose_name_plural = "stock"

    def __str__(self):
        return f"{self.referencia} ({self.tipo})"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="pedidos")
    materiales = models.ManyToManyField(Stock, through="PedidoStock", related_name="pedidos", blank=True)

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_REPARACION = "en_reparacion", "En reparación"
        REPARADO = "reparado", "Reparado"
        ENTREGADO = "entregado", "Entregado"
        SIN_REPARACION = "sin_reparacion", "Sin reparación"

    # Equipo y avería
    equipo = models.TextField()
    numero_serie = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100, blank=True)
    problema = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    comentarios = models.TextField(blank=True)

    # Fechas
    fecha_entrada = models.DateField(default=timezone.localdate)
    fecha_reparacion = models.DateField(null=True, blank=True)
    fecha_pagado = models.DateField(null=True, blank=True)
    tiempo_reparacion = models.PositiveIntegerField(null=True, blank=True)

    # Precio y cobro
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_cobro = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    precio_desglose = models.JSONField(default=dict, blank=True)

    # Garantía
    garantia = models.BooleanField(default=False)
    tiempo_garantia = models.PositiveIntegerField(null=True, blank=True)
    entrega_ref = models.CharField(max_length=100, blank=True)
    ref_garantia = models.CharField(max_length=100, blank=True)
    fecha_entrada_garantia = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_entrada"]

    def __str__(self):
        return f"#{self.pk} {self.equipo} ({self.cliente})"

class PedidoStock(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    cantidad_usada = models.PositiveIntegerField()

    class Meta:
        verbose_name = "material usado"
        verbose_name_plural = "materiales usados"
        constraints = [
            models.UniqueConstraint(fields=["pedido", "stock"], name="pieza_unica_por_pedido"),
        ]

    def __str__(self):
        return f"{self.cantidad_usada} x {self.stock}"
