from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# LOGIN
def login(request):
    return HttpResponse(render(request, "login.html"))

# INTERFACES DE ENFERMERO
def pacientesEnfermero(request):
    return HttpResponse(render(request, "pacientesEnfermero.html"))

def registroPaciente(request):
    return HttpResponse(render(request, "registroPaciente.html"))

def registroEstudiosyGabinete(request):
    return HttpResponse(render(request, "registroEstudiosyGabinete.html"))

def perfilPacienteEnfermero(request):
    return HttpResponse(render(request, "perfilPacienteEnfermero.html"))


# INTERFACES DE MEDICO

def registroTratamiento(request):
    return HttpResponse(render(request, "registroTratamiento.html"))

def pacientesMedico(request):
    return HttpResponse(render(request, "pacientesMedico.html"))

def perfilPacienteMedico(request):
    return HttpResponse(render(request, "perfilPacienteMedico.html"))

# INTERFACES DE ADMINISTRADOR

def registroUsuario(request):
    return HttpResponse(render(request, "registroUsuario.html"))

def perfilUsuario(request):
    return HttpResponse(render(request, "perfilUsuario.html"))

def usuarios(request):
    return HttpResponse(render(request, "usuarios.html"))

# INTERFACES VISTA GENERAL
def signosVitales(request):
    return HttpResponse(render(request, "signosVitales.html"))

def radiografia(request):
    return HttpResponse(render(request, "radiografia.html"))

def estudio(request):
    return HttpResponse(render(request, "estudio.html"))

def estudiosyGabinete(request):
    return HttpResponse(render(request, "estudiosyGabinete.html"))

