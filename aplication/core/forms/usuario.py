from django import forms
from django.forms import ModelForm
from aplication.core.models import Usuario

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'cedula', 'telefono', 'correo', 'direccion']

        error_messages = {
            "cedula": {
                "unique": "Esta cedula ya está en uso"
            },
            "correo": {
                "unique": "Este correo ya está en uso"
            },
            "telefono": {
                "unique": "Este teléfono ya está en uso"
            }
        }

        widgets = {
            "nombres": forms.TextInput(attrs={
                "placeholder": "Escriba los nombres del usuario",
                "id": "id_nombres",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "apellidos": forms.TextInput(attrs={
                "placeholder": "Ingrese los apellidos del usuario",
                "id": "id_apellidos",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "cedula": forms.TextInput(attrs={
                "placeholder": "Ingrese la cédula",
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            "telefono": forms.TextInput(attrs={
                "placeholder": "Ingrese el teléfono",
                "id": "id_telefono",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "correo": forms.EmailInput(attrs={
                "placeholder": "Ingrese el correo",
                "id": "id_correo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Ingrese la dirección",
                "id": "id_direccion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
        }
