"""
URL configuration for Hospital_Infantil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegistroPaciente, RegistroUsuario, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Manejo de usuarios
    path('', include('django.contrib.auth.urls')),

    # Login view
    path('', CustomLoginView.as_view(), name='login'),

    # Logout view
    path('logout/', LogoutView.as_view(), name='logout'),

    # Mostrar usuarios
    path('usuarios/', views.mostrarUsuarios, name='mostrarUsuarios'),



    # INTERFACES DE ENFERMERO
    # Mostrar pacientesEnfermero
    path('pacientesEnfermero/', views.mostrarPacientesEnfermero, name='mostrarPacientesEnfermero'),
    path('registroPaciente/', RegistroPaciente.as_view(), name="registroPaciente"),


    path('registroEstudiosyGabinete/', views.registroEstudiosyGabinete, name="registroEstudiosyGabinete"),
    path('estudiosyGabineteEnfermero/', views.estudiosyGabineteEnfermero, name="estudiosyGabineteEnfermero"),
    path('agregarEstudio/', views.agregarEstudio, name="agregarEstudio"),
    path('pacientesDeshabiltiados/', views.pacientesDeshabilitados, name="pacientesDeshabilitados"),

    # INTERFACES DE MEDICO
    path('registroTratamiento/', views.registroTratamiento, name="registroTratamiento"),
    path('pacientesMedico/', views.mostrarPacientesMedico, name="mostrarPacientesMedico"),
    path('perfilPacienteMedico/', views.perfilPacienteMedico, name="perfilPacienteMedico"),
    path('estudiosyGabineteMedico/', views.estudiosyGabineteMedico, name="estudiosyGabineteMedico"),

    # INTERFACES DE ADMINISTRADOR
    path('registroUsuario/', RegistroUsuario.as_view(), name="registroUsuario"),
    path('perfilUsuario/<int:id>/', views.perfilUsuario, name="perfilUsuario"),
    path('usuarios/', views.usuarios, name="usuarios"),
    path('usuariosDeshabilitados/', views.usuariosDeshabilitados, name="usuariosDeshabilitados"),

    #INTERFACES GENERALES
    path('signosVitales/', views.signosVitales, name="signosVitales"),
    path('radiografia/', views.radiografia, name="radiografia"),
    path('estudio/', views.estudio, name="estudio"),

    path('perfilPacienteEnfermero/<int:expediente>/', views.perfilPacienteEnfermero, name="perfilPacienteEnfermero"),
    path('perfilPacienteMedico/<int:expediente>/', views.perfilPacienteMedico, name="perfilPacienteMedico")
]
