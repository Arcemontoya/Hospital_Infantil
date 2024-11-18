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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegistroPaciente, RegistroUsuario, CustomLoginView, RegistroTratamiento, edicionTratamiento, \
    edicionPaciente, logout_view, listaTratamientos, RegistroEstudios, RegistroRadiografias

urlpatterns = [
    path('admin/', admin.site.urls),

    # Manejo de usuarios
    path('', include('django.contrib.auth.urls')),

    # Login view
    path('', CustomLoginView.as_view(), name='login'),

    # Logout view
    path('logout_view/', views.logout_view, name='logout_view'),

    # Mostrar usuarios
    path('usuarios/', views.mostrarUsuarios, name='mostrarUsuarios'),



    # ------------------------------------------------| INTERFACES DE ENFERMERO |------------------------------------------------
    # Mostrar pacientesEnfermero
    path('pacientesEnfermero/', views.mostrarPacientesEnfermero, name='mostrarPacientesEnfermero'),
    path('registroPaciente/', RegistroPaciente.as_view(), name="registroPaciente"),
    path('pacientes/editar/<int:expediente>/', views.edicionPaciente, name="editarPaciente"),
    path('registroEstudios/<int:expediente>/', RegistroEstudios.as_view(), name="registroEstudios"),
    path('registroRadiografias/<int:expediente>/', RegistroRadiografias.as_view(), name="registroRadiografias"),
    path('pacientesDeshabiltados/', views.pacientesDeshabilitados, name="pacientesDeshabilitados"),
    path('estudioyGabineteEnfermero/<int:expediente>/', views.estudios_GabineteEnfermero, name="estudioyGabineteEnfermero"),

    # ------------------------------------------------| INTERFACES DE MEDICO |------------------------------------------------
    path('paciente/<int:expediente>/agregar_tratamiento/', RegistroTratamiento.as_view(), name='agregarTratamiento'),
    path('pacientesMedico/', views.mostrarPacientesMedico, name="mostrarPacientesMedico"),
    path('perfilPacienteMedico/', views.perfilPacienteMedico, name="perfilPacienteMedico"),
    path('paciente/<int:expediente>/editar_tratamiento/<int:id_tratamiento>/', views.edicionTratamiento, name='edicionTratamiento'),
    path('paciente/<int:expediente>/listaTratamiento/', views.listaTratamientos, name='listaTratamientos'),

    # ------------------------------------------------| INTERFACES DE ADMINISTRADOR |------------------------------------------------
    path('registroUsuario/', RegistroUsuario.as_view(), name="registroUsuario"),
    path('perfilUsuario/<int:id>/', views.perfilUsuario, name="perfilUsuario"),
    path('usuarios/', views.usuarios, name="usuarios"),
    path('usuariosDeshabilitados/', views.usuariosDeshabilitados, name="usuariosDeshabilitados"),
    path('edicion_Usuario/<int:id>/', views.edicionUsuario, name="edicionUsuario"),

    # ------------------------------------------------| INTERFACES GENERALES |------------------------------------------------
    path('signosVitales/', views.signosVitales, name="signosVitales"),
    path('radiografia/', views.radiografia, name="radiografia"),
    path('estudio/', views.estudio, name="estudio"),

    path('perfilPacienteEnfermero/<int:expediente>/', views.perfilPacienteEnfermero, name="perfilPacienteEnfermero"),
    path('perfilPacienteMedico/<int:expediente>/', views.perfilPacienteMedico, name="perfilPacienteMedico")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)