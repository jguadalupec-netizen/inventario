from django.urls import reverse_lazy
from aplication.core.forms.categoria import CategoriaForm
from aplication.core.models import Categoria
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class CategoriaListView(LoginRequiredMixin,ListView):
    model = Categoria
    template_name = 'core/categoria/list.html'
    context_object_name = 'categorias'
    query= None
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return Categoria.objects.filter(
                Q(descripcion__icontains=self.query) 
            )
        return Categoria.objects.all()

class CategoriaCreateView(LoginRequiredMixin,CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria/form.html'
    success_url = reverse_lazy('core:categoria_list')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear categoria"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:categoria_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria=self.object
        messages.success(self.request, f'Categoria creado exitosamente: {categoria.descripcion}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la Categoria. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class CategoriaUpdateView(LoginRequiredMixin,UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria/form.html'
    success_url = reverse_lazy('core:categoria_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Actualizar la Categoria'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria = self.object
        messages.success(self.request, f'Categoria actualizada exitosamente: {categoria.descripcion}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar la Categoria. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    model = Categoria
    template_name = 'includes/confirm_delete_modal.html'
    success_url = reverse_lazy('core:categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Eliminar La Categoria'
        context['description'] = f"¿Desea Eliminar la Categoria: {self.object.descripcion}?"
        context['back_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Categoria eliminada exitosamente.")
        return super().post(request, *args, **kwargs)
