from django.urls import reverse_lazy
from aplication.core.forms.tipo_objeto import TipoObjetoForm
from aplication.core.models import TipoObjeto
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class Tipo_ObjetoListView(LoginRequiredMixin,ListView):
    model = TipoObjeto
    template_name = 'core/tipo_objeto/list.html'
    context_object_name = 'tipos'
    query= None
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return TipoObjeto.objects.filter(
                Q(nombre__icontains=self.query) 
            )
        return TipoObjeto.objects.all()

class Tipo_ObjetoCreateView(LoginRequiredMixin, CreateView):
    model = TipoObjeto
    form_class = TipoObjetoForm
    template_name = 'core/tipo_objeto/form.html'
    success_url = reverse_lazy('core:tipo_objeto_list')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear Tipo De Objeto"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:tipo_objeto_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo=self.object
        messages.success(self.request, f'Tipo de objeto creado exitosamente: {tipo.nombre}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el tipo de objeto. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))
    
class Tipo_ObjetoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoObjeto
    form_class = TipoObjetoForm
    template_name = 'core/tipo_objeto/form.html'
    success_url = reverse_lazy('core:tipo_objeto_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Actualizar el tipo de Objeto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo = self.object
        messages.success(self.request, f'Tipo de objeto actualizado exitosamente: {tipo.nombre}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el tipo de objeto. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class Tipo_objetoDeleteView(LoginRequiredMixin,DeleteView):
    model = TipoObjeto
    template_name = 'includes/confirm_delete_modal.html'
    success_url = reverse_lazy('core:tipo_objeto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Eliminar El tipo de Objeto'
        context['description'] = f"¿Desea Eliminar el Tipo de objeto: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Tipo de objeto eliminado exitosamente.")
        return super().post(request, *args, **kwargs)
