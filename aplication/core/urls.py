from django.urls import path,include
from aplication.core.views.home import HomeTemplateView
from aplication.core.views.usuario import UsuarioCreateView,UsuarioListView,UsuarioUpdateView,UsuarioDeleteView
from aplication.core.views.tipo_objeto import Tipo_ObjetoCreateView,Tipo_ObjetoListView,Tipo_ObjetoUpdateView,Tipo_objetoDeleteView
from aplication.core.views.categoria import CategoriaCreateView,CategoriaListView,CategoriaUpdateView,CategoriaDeleteView
from aplication.core.views.item import ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView
from aplication.core.views.inventario import InventarioListView, InventarioCreateView, InventarioUpdateView, InventarioDeleteView
from aplication.core.views.movimiento import MovimientoListView, MovimientoCreateView, MovimientoUpdateView
app_name = 'core'

urlpatterns = [
    path('', HomeTemplateView.as_view(),name='home'),
    path('usuario_list/',UsuarioListView.as_view() ,name="usuario_list"),
    path('usuario_create/',UsuarioCreateView.as_view() ,name="usuario_create"),
    path('usuario_update/<int:pk>/',UsuarioUpdateView.as_view() ,name="usuario_update"),
    path('usuario_delete/<int:pk>/',UsuarioDeleteView.as_view() ,name="usuario_delete"),
    path('tipo_objeto_list/',Tipo_ObjetoListView.as_view() ,name="tipo_objeto_list"),
    path('tipo_objeto_create/',Tipo_ObjetoCreateView.as_view() ,name="tipo_objeto_create"),
    path('tipo_objeto_update/<int:pk>/',Tipo_ObjetoUpdateView.as_view() ,name="tipo_objeto_update"),
    path('tipo_objeto_delete/<int:pk>/',Tipo_objetoDeleteView.as_view() ,name="tipo_objeto_delete"),
    path('categoria_list/',CategoriaListView.as_view() ,name="categoria_list"),
    path('categoria_create/',CategoriaCreateView.as_view() ,name="categoria_create"),
    path('categoria_update/<int:pk>/',CategoriaUpdateView.as_view() ,name="categoria_update"),
    path('categoria_delete/<int:pk>/',CategoriaDeleteView.as_view() ,name="categoria_delete"),
    path('item_list/', ItemListView.as_view(), name='item_list'),
    path('item_create/', ItemCreateView.as_view(), name='item_create'),
    path('item_update/<int:pk>/', ItemUpdateView.as_view(), name='item_update'),
    path('item_delete/<int:pk>/', ItemDeleteView.as_view(), name='item_delete'),
    path('inventario_list/', InventarioListView.as_view(), name='inventario_list'),
    path('inventario_create/', InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario_update/<int:pk>/', InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario_delete/<int:pk>/', InventarioDeleteView.as_view(), name='inventario_delete'),
    path('movimiento_list/', MovimientoListView.as_view(), name='movimiento_list'),
    path('movimiento_create/', MovimientoCreateView.as_view(), name='movimiento_create'),
    path('movimiento_update/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_update'),
    
]