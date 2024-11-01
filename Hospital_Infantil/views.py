from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegisterForm, PacienteForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

from .models import Paciente


# LOGIN
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('usuarios')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'login.html', {'form': form})


# INTERFACES DE ENFERMERO
def pacientesEnfermero(request):
    return HttpResponse(render(request, "pacientesEnfermero.html"))

def registroPaciente(request):
    if (request == 'POST'):
        form = PacienteForm(request.POST)
        form.save()
        return redirect('Paciente')
    else:
        form = PacienteForm()

    return render(request, "registroPaciente.html", context={'form':form})

def registroEstudiosyGabinete(request):
    return HttpResponse(render(request, "registroEstudiosyGabinete.html"))

def perfilPacienteEnfermero(request):
    return HttpResponse(render(request, "perfilPacienteEnfermero.html"))

def agregarEstudio(request):
    return HttpResponse(render(request, "agregarEstudio.html"))

def estudiosyGabineteEnfermero(request):
    return HttpResponse(render(request, "estudiosyGabineteEnfermero.html"))

def pacientesDeshabilitados(request):
    return HttpResponse(render(request, "pacientesDeshabilitados.html")),

# INTERFACES DE MEDICO

def registroTratamiento(request):
    return HttpResponse(render(request, "registroTratamiento.html"))

def pacientesMedico(request):
    return HttpResponse(render(request, "pacientesMedico.html"))

def perfilPacienteMedico(request):
    return HttpResponse(render(request, "perfilPacienteMedico.html"))

def estudiosyGabineteMedico(request):
    return HttpResponse(render(request, "estudiosyGabineteMedico.html"))


# INTERFACES DE ADMINISTRADOR

def registroUsuario(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('usuarios')
    else:
        form = RegisterForm()
    return render(request, "registroUsuario.html", {"form": form})

def perfilUsuario(request):
    return HttpResponse(render(request, "perfilUsuario.html"))

def usuarios(request):
    return render(request, "usuarios.html")

def usuariosDeshabilitados(request):
    return HttpResponse(render(request, "usuariosDeshabilitados.html"))

# INTERFACES VISTA GENERAL
def signosVitales(request):
    return HttpResponse(render(request, "signosVitales.html"))

def radiografia(request):
    return HttpResponse(render(request, "radiografia.html"))

def estudio(request):
    return HttpResponse(render(request, "estudio.html"))


# MUESTRA DE USUARIOS

def mostrarUsuarios(request):
    users = User.objects.all()
    return render(request, "usuarios.html", {"users": users})

def mostrarPacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, "pacientesEnfermero.html", context={"pacientes": pacientes})
