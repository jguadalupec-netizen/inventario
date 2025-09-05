from datetime import date
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from aplication.core.utils import valida_cedula, phone_regex


class TipoObjeto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"


class Categoria(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Item(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo_objeto = models.ForeignKey(TipoObjeto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    Fecha_hora_de_ingreso = models.DateTimeField(auto_now_add=True)  # <-- Nuevo campo

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.tipo_objeto.nombre} - {self.categoria.descripcion} - Ingresado el: {self.Fecha_hora_de_ingreso.strftime('%d/%m/%Y %H:%M:%S')}"

class Inventario(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item.nombre} - Stock: {self.stock} - Activo: {self.activo}"


class Usuario(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True, validators=[valida_cedula])
    telefono = models.CharField(max_length=10, blank=True, null=True, validators=[phone_regex])
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula} - {self.correo} - {self.telefono} - {self.direccion}"


class Movimiento(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("entregado", "Entregado"),
        ("devuelto", "Devuelto"),
    )

    usuario_entrega = models.ForeignKey(Usuario, related_name="movimientos_entregados", on_delete=models.CASCADE)
    usuario_recibe = models.ForeignKey(Usuario, related_name="movimientos_recibidos", on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField(blank=True, null=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    observaciones = models.TextField(blank=True, null=True)
    codigo_equipo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Movimiento {self.id} - {self.estado} - {self.fecha_entrega} - Entregado por: {self.usuario_entrega} - Recibido por: {self.usuario_recibe} - Código de equipo: {self.codigo_equipo}"

class MovimientoDetalle(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    inventario = models.ManyToManyField(Inventario)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Detalle {self.id} - {self.movimiento} - Inventario: {', '.join([inv.item.nombre for inv in self.inventario.all()])} - Cantidad: {self.cantidad}"