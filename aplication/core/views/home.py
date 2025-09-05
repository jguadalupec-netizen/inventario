from django.views.generic import TemplateView
from aplication.core.models import Item,Usuario
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"title": "Sistema De Gestion De Inventario","title1": "Sistema Inventario", "title2": "Sistema Inventario"}
        ultimo_item = Item.objects.order_by('-id').first()
        context['cant_usuarios'] = Usuario.objects.count()
        if ultimo_item:
            context['ultimo_item_nombre'] = ultimo_item.nombre
            context['ultimo_item_tipo_objeto'] = ultimo_item.tipo_objeto.nombre
            context['ultimo_item_categoria'] = ultimo_item.categoria.descripcion
            context['cantidad_de_items'] = Item.objects.count()
            context['ultimo_item_fecha_hora_ingreso'] = ultimo_item.Fecha_hora_de_ingreso
        ultim_categoria = Item.objects.order_by('-id').first()
        if ultim_categoria:
            context['ultim_categoria_nombre'] = ultim_categoria.categoria.descripcion
        return context
    
        return context