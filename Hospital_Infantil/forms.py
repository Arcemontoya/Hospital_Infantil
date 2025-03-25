from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


from .models import Paciente, Tratamiento, UserProfile, Estudios, Radiografias, HistorialAplicacion
from .Notificaciones import ManejadorNotificaciones


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

class EditUserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese correo electrónico.'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre de usuario.'})
    )
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
class UserProfileForm(forms.ModelForm):

    fecha_registro = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de ingreso.'}),
        required=True
    )

    cedula_profesional = forms.DecimalField(
        max_digits=8,
        decimal_places=0,
        widget = forms.NumberInput(attrs={'placeholder': 'Ingrese el número de cedula profesional.'})
    )

    funcionalidad = forms.ChoiceField(
        choices=UserProfile.FUNCIONALIDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese la funcionalidad del nuevo usuario.'})

    )

    class Meta:
        model = UserProfile
        fields = ['fecha_registro', 'cedula_profesional', 'funcionalidad']

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
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese apellido materno.'}),
    )

    fecha_ingreso = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de ingreso.'}),
    )

    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de ingreso.'}),
    )

    cirugia_realizada = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese cirugia realizada.'})
    )


    peso = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el peso en kilogramos del paciente.'})
    )

    altura = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese la altura en metros del paciente.'})
    )

    diagnostico_clinico_prequirurgico = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese el diagnóstico clínico prequirúrgico.'})
    )

    nota_enfermeria = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese la nota de enfermería.'})
    )

    enfermeros_Encargados = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(user__userprofile__funcionalidad="enfermero"),
        required=False # Modificar
    )

    medico_Encargado = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(funcionalidad='medico'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona el médico encargado.'}),
        empty_label='Seleccionar médico'
    )

    class Meta:
        model = Paciente
        fields = ["nombre", "apellido_paterno", "apellido_materno", "fecha_ingreso", "fecha_nacimiento",
                  "cirugia_realizada", "peso", "altura", "diagnostico_clinico_prequirurgico", "nota_enfermeria", "enfermeros_Encargados", "medico_Encargado"]


class TratamientoForm(forms.ModelForm):
    nombre_Medicamento = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Ingrese el nombre del medicamento.'})
    )

    dosis_Administrada = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese dosis administrada.'})
    )

    # Valida para que máximo sea 60
    frecuencia_Dosis = forms.CharField(
        required=True,
        widget=forms.TextInput
    )

    # Valida para que máximo sea hasta 30 días
    duracion_Terapia = forms.CharField(
        required=True,
        widget=forms.TextInput
    )

    otras_Indicaciones = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese otras indicaciones.'})
    )

    # Este los manejará el enfermero
    """
    historial_aplicacion = forms.DateTimeField(
        required=False,
        initial=timezone.localtime,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M:%S',  # Formato para la fecha y hora
            attrs={
                'type': 'datetime-local',  # Activa un selector de fecha y hora en navegadores modernos
            }
        )
    )
    """

    class Meta:
        model = Tratamiento
        fields = ['nombre_Medicamento', 'dosis_Administrada', 'via_Administracion', 'frecuencia_Dosis',
                  'tiempo_Dosis', 'duracion_Terapia', 'otras_Indicaciones', "tratamiento_activo"]

        widgets = {
            'via_Administracion' : forms.Select(
                attrs={
                    'class': 'form_control',
                    'placeholder': 'Selecciona una opción.'
                }
            ),

            'tiempo_Dosis' : forms.Select(
                attrs={
                    'class': 'form_control',
                    'placeholder': 'Selecciona una opción.'
                }
            ),

            'tratamiento_activo' : forms.Select(
                attrs={
                    'class': 'form_control',
                    'placeholder': 'Selecciona el estado del tratamiento.'
                }
            )
        }


class SuministroTratamiento(forms.ModelForm):
    fecha_aplicacion = forms.DateTimeField(
        required=False,
        initial=timezone.localtime,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M:%S',  # Formato para la fecha y hora
            attrs={
                'type': 'datetime-local',  # Activa un selector de fecha y hora en navegadores modernos
            }
        )
    )

    class Meta:
        model = HistorialAplicacion
        fields = ["fecha_aplicacion"]

class EstudiosForm(forms.ModelForm):
    nombre_Estudio = forms.CharField(

        required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Ingrese el nombre del estudio.'}),
    )

    fecha_realizada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de realización del estudio.'})
    )

    class Meta:
        model = Estudios
        fields= ["nombre_Estudio", "fecha_realizada", "estudio"]

class RadiografiasForm(forms.ModelForm):
    nombre_Radiografia = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Ingrese el nombre de la radiografía.'}),
    )

    fecha_realizada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ingrese fecha de realización de la radiografía.'})
    )
    class Meta:
        model = Radiografias
        fields= ["nombre_Radiografia", "fecha_realizada", "radiografia"]