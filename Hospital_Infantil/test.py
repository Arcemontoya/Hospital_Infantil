from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import (
    RegisterForm, UserProfileForm, PacienteForm, TratamientoForm,
    EstudiosForm, RadiografiasForm
)
from .models import UserProfile, Paciente, Tratamiento, Estudios, Radiografias
from .views import deshabilitar_Usuario


class TestForms(TestCase):

    def test_register_form_valid(self):
        form = RegisterForm(data={
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_email(self):
        form = RegisterForm(data={
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "invalidemail",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertFalse(form.is_valid())

    def test_user_profile_form_valid(self):
        user_profile = UserProfile.FUNCIONALIDAD_CHOICES[0][0]  # Choose first functionality option
        form = UserProfileForm(data={
            "fecha_registro": "2024-12-04",
            "cedula_profesional": "12345678",
            "funcionalidad": user_profile,
        })
        self.assertTrue(form.is_valid())

    def test_user_profile_form_missing_field(self):
        form = UserProfileForm(data={
            "fecha_registro": "2024-12-04",
            "cedula_profesional": "12345678",
        })
        self.assertFalse(form.is_valid())


    def test_paciente_form_valid(self):
        # Crea un usuario
        user = User.objects.create_user(username='medico_test', password='test123')

        # Crea un UserProfile asociado al usuario
        medico = UserProfile.objects.create(
            user=user,  # Asegúrate de pasar el usuario creado
            funcionalidad='medico',
            cedula_profesional="12345678"
        )

        # Ahora puedes crear el formulario
        form = PacienteForm(data={
            "nombre": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "López",
            "fecha_ingreso": "2024-12-01",
            "fecha_nacimiento": "2010-06-15",
            "cirugia_realizada": "Apendicectomía",
            "peso": 70.5,
            "altura": 1.75,
            "diagnostico_clinico_prequirurgico": "Apendicitis aguda",
            "nota_enfermeria": "Paciente estable",
            "medico_Encargado": medico.id,  # Usa el id de UserProfile
        })
        self.assertTrue(form.is_valid())

    def test_tratamiento_form_valid(self):
        form = TratamientoForm(data={
            "nombre_Medicamento": "Paracetamol",
            "dosis_Administrada": "500mg",
            "via_Administracion": "Oral",
            "frecuencia_Dosis": "Cada 8 horas",
            "tiempo_Dosis": "1 semana",
            "duracion_Terapia": "7 días",
            "otras_Indicaciones": "Tomar con alimentos",
        })
        self.assertTrue(form.is_valid())

    def test_estudios_form_valid(self):
        form = EstudiosForm(data={
            "nombre_Estudio": "Electrocardiograma",
            "fecha_realizada": "2024-12-01",
        })
        self.assertTrue(form.is_valid())

    def test_estudios_form_invalid_missing_fields(self):
        form = EstudiosForm(data={
            "fecha_realizada": "2024-12-01",
        })
        self.assertFalse(form.is_valid())

    def test_radiografias_form_valid(self):
        form = RadiografiasForm(data={
            "nombre_Radiografia": "Radiografía de tórax",
            "fecha_realizada": "2024-12-01",
        })
        self.assertTrue(form.is_valid())

    def test_radiografias_form_invalid_missing_fields(self):
        form = RadiografiasForm(data={
            "fecha_realizada": "2024-12-01",
        })
        self.assertFalse(form.is_valid())

