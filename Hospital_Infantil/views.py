import profile

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from .forms import RegisterForm, PacienteForm, UserProfileForm, TratamientoForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

from .models import Paciente, UserProfile, Tratamiento


# --------------------------------------------| LOGIN |--------------------------------------------
class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Obtiene la funcionalidad del perfil de usuario
                user_profile = UserProfile.objects.get(user=user)
                role = user_profile.funcionalidad

                # Redirige según la funcionalidad
                if role == 'administrador':
                    return redirect('usuarios')  # Vista de administrador
                elif role == 'medico':
                    return redirect('mostrarPacientesMedico')  # Vista de médico
                elif role == 'enfermero':
                    return redirect('mostrarPacientesEnfermero')  # Vista de enfermero
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --------------------------------------------| INTERFACES DE ENFERMERO |--------------------------------------------
def pacientesEnfermero(request):
    return render(request, "pacientesEnfermero.html")

class RegistroPaciente(FormView):
    template_name = 'registroPaciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('mostrarPacientesEnfermero')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Usuario registrado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)

def edicionPaciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save(commit=True)
            return redirect('mostrarPacientesEnfermero')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editarPaciente.html', {'form': form, 'paciente': paciente})

def registroEstudiosyGabinete(request):
    return HttpResponse(render(request, "registroEstudiosyGabinete.html"))


def perfilPacienteEnfermero(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientos = Tratamiento.objects.filter(paciente=expediente)
    return render(request, "perfilPacienteEnfermero.html", {'paciente': paciente, 'tratamientos': tratamientos})


def agregarEstudio(request):
    return HttpResponse(render(request, "agregarEstudio.html"))


def estudiosyGabineteEnfermero(request):
    return HttpResponse(render(request, "estudiosyGabineteEnfermero.html"))


def pacientesDeshabilitados(request):
    return HttpResponse(render(request, "pacientesDeshabilitados.html")),


# --------------------------------------------| INTERFACES DE MEDICO |--------------------------------------------

class RegistroTratamiento(FormView):
    template_name = "registroTratamiento.html"
    form_class = TratamientoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.kwargs.get('expediente')
        paciente = get_object_or_404(Paciente, expediente=expediente) if expediente else None
        context['expediente'] = expediente
        context['paciente'] = paciente
        return context

    def form_valid(self, form):
        expediente = self.kwargs.get('expediente')
        paciente = get_object_or_404(Paciente, expediente=expediente)

        # Asociar el tratamiento con el paciente
        tratamiento = form.save(commit=False)
        tratamiento.paciente = paciente
        tratamiento.save()

        # Redirige después de guardar, por ejemplo, a la vista del perfil del paciente
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)

    def get_success_url(self):
        expediente = self.kwargs.get('expediente')
        return reverse_lazy('perfilPacienteMedico', kwargs={'expediente': expediente})

def edicionTratamiento(request, expediente, id_tratamiento):
    # Obtener el paciente y el tratamiento asociado
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamiento = get_object_or_404(Tratamiento, id_Tratamiento=id_tratamiento, paciente=paciente)

    if request.method == 'POST':
        # Crear un formulario con los datos enviados
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()  # Guardar cambios en el tratamiento
            messages.success(request, "Tratamiento editado con éxito.")
            # Redirigir al perfil del paciente después de la edición
            return redirect('perfilPacienteMedico', expediente=paciente.expediente)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        # Crear el formulario con la instancia del tratamiento para editar
        form = TratamientoForm(instance=tratamiento)

    return render(request, 'editarTratamiento.html', {'form': form, 'paciente': paciente, 'tratamiento': tratamiento})

def perfilPacienteMedico(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientos = Tratamiento.objects.filter(paciente=expediente)
    return render(request, "perfilPacienteMedico.html", {'paciente': paciente, 'tratamientos': tratamientos})

def listaTratamientos(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientos = Tratamiento.objects.filter(paciente=expediente)
    return render(request, "listaTratamientos.html", {'paciente': paciente, 'tratamientos': tratamientos})



def estudiosyGabineteMedico(request):
    return HttpResponse(render(request, "estudiosyGabineteMedico.html"))




# --------------------------------------------| INTERFACES DE ADMINISTRADOR |--------------------------------------------

class RegistroUsuario(FormView):
    template_name = 'registroUsuario.html'
    success_url = reverse_lazy('usuarios')
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = UserProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        profile_form = UserProfileForm(self.request.POST)

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        try:
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(self.request, "Usuario registrado con éxito.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error al registrar el usuario: {e}")
            return self.form_invalid(form, profile_form)

    def form_invalid(self, form, profile_form):
        print("Errores en los formularios:")
        print(form.errors)
        print(profile_form.errors)

        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )

def perfilUsuario(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    return render(request, "perfilUsuario.html", {'user': user, 'user_profile': user_profile})


def usuarios(request):
    users = User.objects.select_related('user_profile').all()
    return render(request, "usuarios.html", {'users': users})


# --------------------------------------------| INTERFACES DE VISTA GENERAL |--------------------------------------------

def pacientesDeshabilitados(request):
    return HttpResponse(render(request, "usuariosDeshabilitados.html"))

def usuariosDeshabilitados(request):
    return HttpResponse(render(request, "usuariosDeshabilitados.html"))

def signosVitales(request):
    return HttpResponse(render(request, "signosVitales.html"))


def radiografia(request):
    return HttpResponse(render(request, "radiografia.html"))


def estudio(request):
    return HttpResponse(render(request, "estudio.html"))


# --------------------------------------------| INTERFACES DE MUESTRA DE DATOS |--------------------------------------------

def mostrarUsuarios(request):
    users = User.objects.all()
    return render(request, "usuarios.html", {"users": users})


def mostrarPacientesEnfermero(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientesEnfermero.html', {'Pacientes': pacientes})

def mostrarPacientesMedico(request):
    pacientes = Paciente.objects.filter(medico_Encargado__user=request.user)
    return render(request, 'pacientesMedico.html', {'Pacientes': pacientes})
