from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Paciente


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese correo electrónico.'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre de usuario.'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese contraseña.'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme contraseña.'})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


# ---------------------------------------- | PACIENTES | ------------------------------------------------------------

class PacienteForm(forms.ModelForm):
    nombre = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre.'})
    )
    apellido_paterno = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese apellido paterno.'})
    )
    apellido_materno = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese apellido materno.'})
    )

    fecha_ingreso = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de ingreso.'})
    )

    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de ingreso.'})
    )

    cirugia_realizada = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese cirugia realizada.'})
    )


    peso = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese fecha de ingreso.'})
    )

    altura = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el peso del paciente.'})
    )

    diagnostico_clinico_prequirurgico = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese el diagnóstico clínico prequirúrgico.'})
    )

    nota_enfermeria = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese la nota de enfermería.'})
    )

    class Meta:
        model = Paciente
        fields = ["nombre", "apellido_paterno", "apellido_materno", "fecha_ingreso", "fecha_nacimiento",
                  "cirugia_realizada", "peso", "altura", "diagnostico_clinico_prequirurgico", "nota_enfermeria"]

#class Tratamiento(Model.ModelForm):
