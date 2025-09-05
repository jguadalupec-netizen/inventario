from django.urls import reverse_lazy
from aplication.core.forms.item import ItemForm
from aplication.core.models import Item
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class ItemListView(LoginRequiredMixin,ListView):
    model = Item
    template_name = 'core/item/list.html'
    context_object_name = 'items'
    query= None
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return Item.objects.filter(
                Q(nombre__icontains=self.query) 
            )
        return Item.objects.all()

class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'core/item/form.html'
    success_url = reverse_lazy('core:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear Item"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:item_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo=self.object
        messages.success(self.request, f'Item creado exitosamente: {tipo.nombre}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el item. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))
    
class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'core/item/form.html'
    success_url = reverse_lazy('core:item_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Actualizar el Item'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        item = self.object
        messages.success(self.request, f'Item actualizado exitosamente: {item.nombre}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el item. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class ItemDeleteView(LoginRequiredMixin,DeleteView):
    model = Item
    template_name = 'includes/confirm_delete_modal.html'
    success_url = reverse_lazy('core:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Eliminar El Item'
        context['description'] = f"¿Desea Eliminar el Item: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Item eliminado exitosamente.")
        return super().post(request, *args, **kwargs)