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

from .views import index, RegistroPaciente, RegistroUsuario, CustomLoginView, RegistroTratamiento, \
    logout_view, RegistroEstudios, RegistroRadiografias, \
    desplieguePacientesHabilitados, desplieguePacientesDeshabilitados, edicionPacientes, perfilPaciente, \
    edicionTratamientos, actualizar_historial, EstudiosYGabinete, mostrarRadiografias, eliminar_historial, eliminar_Tratamiento
     

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

    # Recuperar contraseña
    path('recuperarCuenta/', views.recuperarCuenta, name='recuperarCuenta'),

    path('verificarCodigo/', views.verificarCodigo, name="verificarCodigo"),

    path('cambiarPassword/', views.cambiarPassword, name='cambiarPassword'),

    # Notificaciones
    path('verNotificaciones/', views.verNotificaciones, name='verNotificaciones'),

    # ------------------------------------------------| INTERFACES DE ENFERMERO |------------------------------------------------
    # Mostrar pacientesEnfermero
    path('registroPaciente/', RegistroPaciente.as_view(), name="registroPaciente"),
    path('pacientes/editar/<int:expediente>/', edicionPacientes.as_view(), name="editarPaciente"),
    path('registroEstudios/<int:expediente>/', RegistroEstudios.as_view(), name="registroEstudios"),
    path('registroRadiografias/<int:expediente>/', RegistroRadiografias.as_view(), name="registroRadiografias"),
    path('ver_pdfEstudios/<int:id_Estudio>/', views.ver_pdfEstudios, name='ver_pdfEstudios'),
    path('ver_pdfRadiografias/<int:id_Radiografia>/', views.ver_pdfRadiografias, name='ver_pdfRadiografias'),
    path('paciente/<int:expediente>/actualizar_tratamiento/<int:id_tratamiento>/',
         views.actualizacion_Aplicacion_Tratamiento, name="actualizacionTratamiento"),
    path('paciente/pacientesDeshabilitados', desplieguePacientesDeshabilitados.as_view(), name='pacientesDeshabilitados'),
    path('deshabilitarPaciente/<int:expediente>', views.deshabilitarPaciente, name='deshabilitarPaciente'),
    path('habilitarPaciente/<int:expediente>', views.habilitarPaciente, name="habilitarPaciente"),

    # ------------------------------------------------| INTERFACES DE MEDICO |------------------------------------------------
    path('paciente/<int:expediente>/agregar_tratamiento/', RegistroTratamiento.as_view(), name='agregarTratamiento'),
    path('paciente/<int:expediente>/editar_tratamiento/<int:pk>/', edicionTratamientos.as_view(), name = "edicionTratamiento"),

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


    # ------------------------------------------------| URL REFACTOR |------------------------------------------------

    path('pacientes/', desplieguePacientesHabilitados.as_view(), name='pacientes'),
    path('pacientes/<int:expediente>/', perfilPaciente.as_view(), name="perfilPaciente"),
    path('pacientes/<int:expediente>/editar/', edicionPacientes.as_view(), name="editarPaciente"),
    path('pacientes/<int:expediente>/estudiosyGabinete/', EstudiosYGabinete.as_view(), name='estudiosyGabinete'),
    path('radiografia/<int:expediente>/<int:id_Radiografia>/', views.mostrarRadiografias, name='radiografia'),
    path('estudio/<int:expediente>/<int:id_Estudio>/', views.mostrarEstudios, name='estudio'),
    path('estudio/<int:id_Estudio>/delete/', views.delete_pdfEstudios, name='delete_pdfEstudios'),
    path('estudio/<int:id_Estudio>/replace/', views.replace_pdfEstudios, name='replace_pdfEstudios'),

    path('editar_historial/<int:id>/', actualizar_historial, name='editar_historial'),
    path('eliminar_historial/<int:id>/', eliminar_historial, name='eliminar_historial'),
    path('eliminar_tratamiento/<int:id_Tratamiento>/', eliminar_Tratamiento, name='eliminar_tratamiento'),
    path("actualizar-historial/<int:id>/", actualizar_historial, name="actualizar_historial"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)