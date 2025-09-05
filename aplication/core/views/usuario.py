from django.urls import reverse_lazy
from aplication.core.forms.usuario import UsuarioForm
from aplication.core.models import Usuario
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class UsuarioListView( LoginRequiredMixin,ListView):
    model = Usuario
    template_name = 'core/usuario/list.html'
    context_object_name = 'usuarios'
    query= None
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        if self.query:
            return Usuario.objects.filter(
                Q(nombres__icontains=self.query) | 
                Q(apellidos__icontains=self.query) | 
                Q(cedula__icontains=self.query) | 
                Q(correo__icontains=self.query)
            )
        return Usuario.objects.all()
    
class UsuarioCreateView(LoginRequiredMixin,CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'core/usuario/form.html'
    success_url = reverse_lazy('core:usuario_create')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear Usuario"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:usuario_list")
        return context


    def form_valid(self, form):
        response = super().form_valid(form)
        usuario=self.object
        messages.success(self.request, f'Usuario creado exitosamente: {usuario.nombres}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el usuario. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class UsuarioUpdateView( LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'core/usuario/form.html'
    success_url = reverse_lazy('core:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "Crear Usuario"
        context["grabar"] = "Guardar"
        context["back_url"] = reverse_lazy("core:usuario_list")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        usuario = self.object
        messages.success(self.request, f'Usuario actualizado exitosamente: {usuario.nombres}')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el usuario. Por favor, corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

class UsuarioDeleteView(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = 'includes/confirm_delete_modal.html'
    success_url = reverse_lazy('core:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema De Gestion De Inventario"
        context['grabar'] = 'Eliminar el usuario'
        context['description'] = f"¿Desea Eliminar el usuario: {self.object.nombres}?"
        context['back_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Usuario eliminado exitosamente.")
        return super().post(request, *args, **kwargs)

    