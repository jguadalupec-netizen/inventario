from django import forms
from django.forms import ModelForm
from aplication.core.models import Inventario

class InventarioForm(ModelForm):
    class Meta:
        model = Inventario
        fields = ['item', 'stock', 'activo']

        widgets = {
            "item": forms.Select(attrs={
                "id": "id_item",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg "
                         "focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 "
                         "dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 "
                         "dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 "
                         "dark:shadow-sm-light",
            }),
            "stock": forms.NumberInput(attrs={
                "placeholder": "Ingrese el stock",
                "id": "id_stock",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg "
                         "focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 "
                         "dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 "
                         "dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 "
                         "dark:shadow-sm-light",
            }),
            "activo": forms.CheckboxInput(attrs={
                "id": "id_activo",
                "class": "form-check-input",
            }),
        }
