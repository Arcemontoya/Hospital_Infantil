from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Paciente


class TestLoginView(TestCase):

    def setUp(self):
        # Crear un usuario de prueba con un perfil de administrador
        self.user = User.objects.create_user(username='admin', password='password')
        self.profile = UserProfile.objects.create(user=self.user, funcionalidad='administrador', cedula_profesional="12345678")

    def test_login_redirect_admin(self):
        # Realizar la solicitud POST para iniciar sesión
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'password'})
        self.assertRedirects(response, reverse('usuarios'))  # Verificar redirección a la vista 'usuarios'

    def test_login_redirect_medico(self):
        # Crear un usuario con el rol 'medico'
        self.profile.funcionalidad = 'medico'
        self.profile.save()
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'password'})
        self.assertRedirects(response, reverse(
            'mostrarPacientesMedico'))  # Verificar redirección a la vista 'mostrarPacientesMedico'

    def test_login_redirect_enfermero(self):
        # Crear un usuario con el rol 'enfermero'
        self.profile.funcionalidad = 'enfermero'
        self.profile.save()
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'password'})
        self.assertRedirects(response, reverse(
            'mostrarPacientesEnfermero'))  # Verificar redirección a la vista 'mostrarPacientesEnfermero'

## ------------------------------------------ REGISTRO DE PACIENTE ------------------------------------------------------------------------------------
class TestRegistroPaciente(TestCase):

    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='medico1', password='password')
        self.profile = UserProfile.objects.create(user=self.user, funcionalidad='medico', cedula_profesional="12345678")

    def test_registro_paciente_valido(self):
        response = self.client.post(reverse('registroPaciente'), {
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'Gómez',
            'fecha_ingreso': '2024-12-01',
            'fecha_nacimiento': '1990-06-15',
            'cirugia_realizada': 'Ninguna',
            'peso': '70',
            'altura': '1.75',
            'diagnostico_clinico_prequirurgico': 'Diagnóstico',
            'nota_enfermeria': 'Nota de enfermería',
            'medico_Encargado': self.profile.id  # Usando el ID del médico creado
        })
        self.assertRedirects(response, reverse('mostrarPacientesEnfermero'))

    def test_registro_paciente_invalido(self):
        # Enviar datos del formulario con un campo requerido vacío
        response = self.client.post(reverse('registroPaciente'), {
            'nombre': '',  # Dejar vacío el campo nombre para que falle la validación
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'Gómez',
            'fecha_ingreso': '2024-12-01',
            'fecha_nacimiento': '1990-06-15',
            'cirugia_realizada': 'Ninguna',
            'peso': '70',
            'altura': '1.75',
            'diagnostico_clinico_prequirurgico': 'Diagnóstico',
            'nota_enfermeria': 'Nota de enfermería',
            'medico_Encargado': '1'  # Asegúrate de que el ID sea válido
        })

        # Acceder al formulario desde el contexto
        form = response.context['form']  # Aquí es donde se guarda el formulario en el contexto

        # Verificar que el error esté presente en el campo 'nombre'
        self.assertFormError(form, 'nombre', 'Este campo es obligatorio.')


## ---------------------------------------------------------------- EDICION DE PACIENTE -------------------------------------------------------------
class TestEdicionPaciente(TestCase):

    def setUp(self):
        # Crear un paciente de prueba y asociar un usuario
        self.user = User.objects.create_user(username='medico', password='password')
        self.profile = UserProfile.objects.create(user=self.user, funcionalidad='medico', cedula_profesional="12345678")
        self.paciente = Paciente.objects.create(
            expediente='12345', nombre='Pedro', apellido_paterno='Lopez',
            apellido_materno='Martinez', fecha_ingreso='2024-12-01',
            fecha_nacimiento='1990-01-01', cirugia_realizada='Ninguna',
            peso=80, altura=1.80, medico_Encargado=self.profile
        )

    def test_editar_paciente(self):
        # Editar los datos del paciente
        response = self.client.post(reverse('editarPaciente', kwargs={'expediente': self.paciente.expediente}), {
            'nombre': 'Pedro',
            'apellido_paterno': 'Lopez',
            'apellido_materno': 'Martinez',
            'fecha_ingreso': '2024-12-01',
            'fecha_nacimiento': '1990-01-01',
            'cirugia_realizada': 'Ninguna',
            'peso': '85',  # Cambiar el peso
            'altura': '1.80',
            'diagnostico_clinico_prequirurgico': 'Actualización',
            'nota_enfermeria': 'Nota de enfermería',
            'medico_Encargado': self.profile.id
        })
        # Verificar que la redirección se realice correctamente
        self.assertRedirects(response, reverse('mostrarPacientesEnfermero'))
        # Verificar que los cambios se hayan guardado
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.peso, 85)

