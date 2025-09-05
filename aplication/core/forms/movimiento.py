from django import forms
from django.forms import ModelForm
from aplication.core.models import Movimiento

class MovimientoForm(ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            "usuario_entrega",
            "usuario_recibe",
            "fecha_entrega",
            "estado",
            "observaciones",
            "codigo_equipo"
        ]
        widgets = {
            'usuario_entrega': forms.Select(attrs={
                'class': 'form-select shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'id': 'id_usuario_entrega',
            }),
            'usuario_recibe': forms.Select(attrs={
                'class': 'form-select shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'id': 'id_usuario_recibe',
            }),
            'fecha_entrega': forms.DateTimeInput(attrs={
                'class': 'form-control shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'type': 'datetime-local',
                'id': 'id_fecha_entrega',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'id': 'id_estado',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'rows': 3,
                'placeholder': 'Observaciones',
                'id': 'id_observaciones',
            }),
            'codigo_equipo': forms.TextInput(attrs={
                'class': 'form-control shadow-sm bg-gray-50 border border-gray-300 rounded-lg',
                'placeholder': 'Código de equipo',
                'id': 'id_codigo_equipo',
            }),
        }
        labels = {
            "usuario_entrega": "Usuario que entrega",
            "usuario_recibe": "Usuario que recibe",
            "fecha_entrega": "Fecha de entrega",
            "estado": "Estado",
            "observaciones": "Observaciones",
            "codigo_equipo": "Código de equipo",
        }