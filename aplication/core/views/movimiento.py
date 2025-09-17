import json
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Movimiento, MovimientoDetalle, Inventario, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin

class MovimientoListView(LoginRequiredMixin,ListView):
    template_name = "core/movimiento/list.html"
    model = Movimiento
    context_object_name = 'movimientos'

    def get_queryset(self):
        query = Movimiento.objects.all()
        estado = self.request.GET.get('estado')
        usuario = self.request.GET.get('usuario')
        codigo_equipo = self.request.GET.get('codigo_equipo')
        if estado:
            query = query.filter(estado=estado)
        if usuario:
            query = query.filter(usuario_entrega__nombres__icontains=usuario)
        if codigo_equipo:
            query = query.filter(codigo_equipo__icontains=codigo_equipo)
        return query.order_by('-fecha_entrega')

class MovimientoCreateView(LoginRequiredMixin,CreateView):
    model = Movimiento
    template_name = 'core/movimiento/form.html'
    fields = [
        "usuario_entrega", "usuario_recibe", "fecha_entrega",
        "estado", "observaciones", "codigo_equipo"
    ]
    success_url = reverse_lazy('movimiento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['inventarios'] = Inventario.objects.all()
        context['detalle_movimiento'] = []
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        detalles = data.get('detalles', [])
        try:
            with transaction.atomic():
                movimiento = Movimiento.objects.create(
                    usuario_entrega_id=int(data['usuario_entrega']),
                    usuario_recibe_id=int(data['usuario_recibe']),
                    fecha_entrega=timezone.now(),
                    estado=data.get('estado', 'pendiente'),
                    observaciones=data.get('observaciones', ''),
                    codigo_equipo=data.get('codigo_equipo', '')
                )
                for detalle in detalles:
                    inventario_ids = detalle.get('inventario_ids', [])
                    inventarios = Inventario.objects.filter(id__in=inventario_ids)
                    cantidad = int(detalle['cantidad'])
                    # Validar stock suficiente antes de crear el detalle
                    for inventario in inventarios:
                        if inventario.stock < cantidad:
                            raise Exception(f"Stock insuficiente para el inventario '{inventario}'. Stock actual: {inventario.stock}, solicitado: {cantidad}")
                    detalle_obj = MovimientoDetalle.objects.create(
                        movimiento=movimiento,
                        cantidad=cantidad
                    )
                    detalle_obj.inventario.set(inventarios)
                    for inventario in inventarios:
                        inventario.stock -= cantidad
                        inventario.save()
                messages.success(self.request, f"Movimiento #{movimiento.id} registrado correctamente.")
                return JsonResponse({"msg": "Movimiento registrado correctamente."}, status=200)
        except Exception as ex:
            messages.error(self.request, "Error al registrar el movimiento.")
            return JsonResponse({"msg": str(ex)}, status=400)

class MovimientoUpdateView(LoginRequiredMixin,UpdateView):
    model = Movimiento
    template_name = 'core/movimiento/form.html'
    fields = [
        "usuario_entrega", "usuario_recibe", "fecha_entrega",
        "estado", "observaciones", "codigo_equipo"
    ]
    success_url = reverse_lazy('movimiento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['inventarios'] = Inventario.objects.all()
        detalles = list(MovimientoDetalle.objects.filter(movimiento_id=self.object.id).values("id", "cantidad", "inventario__id", "inventario__item__nombre"))
        context['detalle_movimiento'] = json.dumps(detalles)
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        detalles = data.get('detalles', [])
        try:
            movimiento = Movimiento.objects.get(id=self.kwargs.get('pk'))
            with transaction.atomic():
                movimiento.usuario_entrega_id = int(data['usuario_entrega'])
                movimiento.usuario_recibe_id = int(data['usuario_recibe'])
                movimiento.fecha_entrega = timezone.now()
                movimiento.estado = data.get('estado', 'pendiente')
                movimiento.observaciones = data.get('observaciones', '')
                movimiento.codigo_equipo = data.get('codigo_equipo', '')
                movimiento.save()
                # DEVOLVER STOCK de los detalles anteriores antes de eliminarlos
                detalles_anteriores = MovimientoDetalle.objects.filter(movimiento_id=movimiento.id)
                for detalle_ant in detalles_anteriores:
                    for inventario in detalle_ant.inventario.all():
                        inventario.stock += detalle_ant.cantidad
                        inventario.save()
                detalles_anteriores.delete()
                # Crear nuevos detalles y RESTAR stock con validación
                for detalle in detalles:
                    inventario_ids = detalle.get('inventario_ids', [])
                    inventarios = Inventario.objects.filter(id__in=inventario_ids)
                    cantidad = int(detalle['cantidad'])
                    # Validar stock suficiente antes de crear el detalle
                    for inventario in inventarios:
                        if inventario.stock < cantidad:
                            raise Exception(f"Stock insuficiente para el inventario '{inventario}'. Stock actual: {inventario.stock}, solicitado: {cantidad}")
                    detalle_obj = MovimientoDetalle.objects.create(
                        movimiento=movimiento,
                        cantidad=cantidad
                    )
                    detalle_obj.inventario.set(inventarios)
                    for inventario in inventarios:
                        inventario.stock -= cantidad
                        inventario.save()
                messages.success(self.request, f"Movimiento #{movimiento.id} actualizado correctamente.")
                return JsonResponse({"msg": "Movimiento actualizado correctamente."}, status=200)
        except Exception as ex:
            messages.error(self.request, "Error al actualizar el movimiento.")
            return JsonResponse({"msg": str(ex)}, status=400)

# ...existing code...
class MovimientoDetalleJsonView(LoginRequiredMixin, DetailView):
    model = Movimiento

    def get(self, request, *args, **kwargs):
        movimiento = self.get_object()
        # Agrupar cantidades por inventario (por si hay varios detalles que referencian al mismo inventario)
        productos = {}
        detalles_qs = MovimientoDetalle.objects.filter(movimiento=movimiento).prefetch_related('inventario__item')
        for detalle in detalles_qs:
            for inv in detalle.inventario.all():
                key = inv.id
                nombre = getattr(getattr(inv, 'item', None), 'nombre', str(inv))
                productos.setdefault(key, {'nombre': nombre, 'cantidad': 0})
                productos[key]['cantidad'] += detalle.cantidad

        detalles_list = list(productos.values())

        movimiento_data = {
            'id': movimiento.id,
            'usuario_entrega': getattr(getattr(movimiento, 'usuario_entrega', None), 'nombres', str(getattr(movimiento, 'usuario_entrega', ''))),
            'usuario_recibe': getattr(getattr(movimiento, 'usuario_recibe', None), 'nombres', str(getattr(movimiento, 'usuario_recibe', ''))),
            'fecha_entrega': movimiento.fecha_entrega.isoformat() if getattr(movimiento, 'fecha_entrega', None) else None,
            'estado': movimiento.estado,
            'observaciones': movimiento.observaciones,
            'codigo_equipo': movimiento.codigo_equipo,
        }

        return JsonResponse({'movimiento': movimiento_data, 'detalles': detalles_list}, status=200)
# ...existing code...
