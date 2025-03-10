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
    edicionPaciente, logout_view, listaTratamientos, RegistroEstudios, RegistroRadiografias, \
    desplieguePacientesHabilitados, desplieguePacientesDeshabilitados, edicionPacientes, perfilPaciente, \
    edicionTratamientos, actualizar_historial, Pacientes

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

    #Mostrar usuarios deshabilitados
    path('usuariosDeshabilitados/', views.mostrarUsuariosDeshabilitados, name='mostrarUsuariosDeshabilitados'),

    #Mostrar pacientes deshabilitados
    path('pacientesDeshabilitados/', views.mostrarPacientesDeshabilitados, name='mostrarPacientesDeshabilitados'),

    # ------------------------------------------------| TESTING |------------------------------------------------

    #path('estudios/pdf/<int:pk>/', mostrarDetallesEstudios.as_view(), name='ver_pdfEstudios'),
    #path('testing/<int:paciente_id>/', views.EstudiosYGabinete.as_view(), name='name'), así se manda a llamar Estudios y Radiografía combinados
    #path('testing/<int:pk>/', edicionPacientes.as_view(), name = "edicionPacientes"), así se manda a llamar
    #path('testing/<int:expendiente>/<int:pk>', edicionTratamientos.as_view(), name = "perfilPaciente"), Así se edita un medicamento




    # ------------------------------------------------| INTERFACES DE ENFERMERO |------------------------------------------------
    # Mostrar pacientesEnfermero
    path('registroPaciente/', RegistroPaciente.as_view(), name="registroPaciente"),
    path('pacientes/editar/<int:expediente>/', views.edicionPaciente, name="editarPaciente"),
    path('registroEstudios/<int:expediente>/', RegistroEstudios.as_view(), name="registroEstudios"),
    path('registroRadiografias/<int:expediente>/', RegistroRadiografias.as_view(), name="registroRadiografias"),
    path('pacientesDeshabiltados/', views.pacientesDeshabilitados, name="pacientesDeshabilitados"),
    path('estudioyGabineteEnfermero/<int:expediente>/', views.estudios_GabineteEnfermero, name="estudioyGabineteEnfermero"),
    path('estudioEnfermero/<int:expediente>/<int:id_Estudio>/', views.mostrarEstudioEnfermero,
         name='mostrarEstudioEnfermero'),
    path('radiografiaEnfermero/<int:expediente>/<int:id_Radiografia>/', views.mostrarRadiografiaEnfermero, name="mostrarRadiografiaEnfermero"),
    path('ver_pdfEstudios/<int:id_Estudio>/', views.ver_pdfEstudios, name='ver_pdfEstudios'),
    path('ver_pdfRadiografias/<int:id_Radiografia>/', views.ver_pdfRadiografias, name='ver_pdfRadiografias'),
    path('paciente/<int:expediente>/actualizar_tratamiento/<int:id_tratamiento>/',
         views.actualizacion_Aplicacion_Tratamiento, name="actualizacionTratamiento"),
   # path('paciente/<int:expediente>/listaTratamientosEnfermero/', views.listaTratamientosEnfermero, name='listaTratamientosEnfermero'),
    path('paciente/pacientesDeshabilitados', views.pacientesDeshabilitados, name='pacientesDeshabilitados'),
    path('deshabilitarPaciente/<int:expediente>', views.deshabilitarPaciente, name='deshabilitarPaciente'),
    path('habilitarPaciente/<int:expediente>', views.habilitarPaciente, name="habilitarPaciente"),

    path("actualizar-historial/<int:id>/", actualizar_historial, name="actualizar_historial"),

    # ------------------------------------------------| INTERFACES DE MEDICO |------------------------------------------------
    path('paciente/<int:expediente>/agregar_tratamiento/', RegistroTratamiento.as_view(), name='agregarTratamiento'),
    path('perfilPacienteMedico/', views.perfilPacienteMedico, name="perfilPacienteMedico"),
    #path('paciente/<int:expediente>/editar_tratamiento/<int:id_tratamiento>/', views.edicionTratamiento, name='edicionTratamiento'),
    path('paciente/<int:pk>/', edicionTratamientos.as_view(), name = "edicionTratamiento"),
    path('paciente/<int:expediente>/listaTratamiento/', views.listaTratamientos, name='listaTratamientos'),
    path('estudioyGabineteMedico/<int:expediente>/', views.estudios_GabineteMedico,
         name="estudioyGabineteMedico"),
    path('estudio/<int:id_Estudio>/', views.mostrarEstudioMedico, name="mostrarEstudioMedico"),
    path('radiografia/<int:id_Radiografia>/', views.mostrarRadiografiaMedico, name="mostrarRadiografiaMedico"),

    # ------------------------------------------------| INTERFACES DE ADMINISTRADOR |------------------------------------------------
    path('registroUsuario/', RegistroUsuario.as_view(), name="registroUsuario"),
    path('perfilUsuario/<int:id>/', views.perfilUsuario, name="perfilUsuario"),
    path('usuarios/', views.usuarios, name="usuarios"),
    path('usuariosDeshabilitados/', views.usuariosDeshabilitados, name="usuariosDeshabilitados"),
    path('edicion_Usuario/<int:id>/', views.edicionUsuario, name="edicionUsuario"),
    path('deshabilitar_usuario/<int:id>/', views.deshabilitar_Usuario, name='deshabilitar_usuario'),
    path('habilitar_usuario/<int:id>', views.habilitar_Usuario, name='habilitar_usuario'),

    # ------------------------------------------------| INTERFACES GENERALES |------------------------------------------------
    path('signosVitales/', views.signosVitales, name="signosVitales"),

    path('perfilPacienteEnfermero/<int:expediente>/', views.perfilPacienteEnfermero, name="perfilPacienteEnfermero"),
    path('perfilPacienteMedico/<int:expediente>/', views.perfilPacienteMedico, name="perfilPacienteMedico"),


    # ------------------------------------------------| URL REFACTOR |------------------------------------------------

    path('pacientes/', desplieguePacientesHabilitados.as_view(), name='pacientes')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)