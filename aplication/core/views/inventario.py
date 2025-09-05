from django.urls import reverse_lazy
from aplication.core.forms.inventario import InventarioForm
from aplication.core.models import Inventario, TipoObjeto
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class InventarioListView(LoginRequiredMixin,ListView):
    model = Inventario
    template_name = 'core/inventario/list.html'
    context_object_name = 'inventarios'
    query= None
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return Inventario.objects.filter(
                Q(item__nombre__icontains=self.query) 
            )
        return Inventario.objects.all()

class InventarioCreateView(LoginRequiredMixin,CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'core/inventario/form.html'
    success_url = reverse_lazy('core:inventario_list')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear Inventario"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:inventario_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        inventario = self.object
        messages.success(self.request, f'Inventario creado exitosamente: {inventario.item}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el inventario. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))
    
class InventarioUpdateView(LoginRequiredMixin,UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'core/inventario/form.html'
    success_url = reverse_lazy('core:inventario_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Actualizar el Inventario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        inventario = self.object
        messages.success(self.request, f'Inventario actualizado exitosamente: {inventario.item}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el inventario. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class InventarioDeleteView(LoginRequiredMixin,DeleteView):
    model = Inventario
    template_name = 'includes/confirm_delete_modal.html'
    success_url = reverse_lazy('core:inventario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Eliminar El Inventario'
        context['description'] = f"¿Desea Eliminar el Inventario: {self.object.item}?"
        context['back_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Inventario eliminado exitosamente.")
        return super().post(request, *args, **kwargs)
