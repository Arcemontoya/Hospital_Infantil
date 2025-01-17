import profile

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, UpdateView

from .forms import RegisterForm, PacienteForm, UserProfileForm, TratamientoForm, EstudiosForm, RadiografiasForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from django.utils import timezone

from .models import Paciente, UserProfile, Tratamiento, Radiografias, Estudios, HistorialAplicacion


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


def perfilPacienteEnfermero(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientosActivos = Tratamiento.objects.filter(paciente=expediente, tratamiento_activo="activo")
    tratamientosInactivos = Tratamiento.objects.filter(paciente=expediente, tratamiento_activo="Inactivo")
    radiografias = Radiografias.objects.filter(paciente=expediente)
    estudios = Estudios.objects.filter(paciente=expediente)
    return render(request, "perfilPacienteEnfermero.html", {'paciente': paciente, 'tratamientosActivos': tratamientosActivos,
                                                         'tratamientosInactivos': tratamientosInactivos, 'estudios': estudios, 'radiografias': radiografias})


def estudios_GabineteEnfermero(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)

    estudios = Estudios.objects.filter(paciente=paciente)
    radiografias = Radiografias.objects.filter(paciente=paciente)

    return render(request, 'estudiosyGabineteEnfermero.html',
                  context={'paciente': paciente, 'estudios': estudios, 'radiografias': radiografias})

class RegistroEstudios(FormView):
    template_name = 'registroEstudio.html'
    form_class = EstudiosForm

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
        estudio_registro = form.save(commit=False)
        estudio_registro.paciente = paciente
        estudio_registro.save()

        self.success_url = reverse('estudioyGabineteEnfermero', args=[expediente])
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)

class RegistroRadiografias(FormView):
    template_name = 'registroRadiografia.html'
    form_class = RadiografiasForm

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
        estudio_registro = form.save(commit=False)
        estudio_registro.paciente = paciente
        estudio_registro.save()

        self.success_url = reverse('estudioyGabineteEnfermero', args=[expediente])
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)


def ver_pdfEstudios(request, id_Estudio):
    estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    archivo_pdf = estudio.estudio
    response = FileResponse(archivo_pdf.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{archivo_pdf.name}"'

    return response

def ver_pdfRadiografias(request, id_Radiografia):
    radiografia = get_object_or_404(Radiografias, id_Radiografia=id_Radiografia)
    archivo_pdf = radiografia.radiografia
    response = FileResponse(archivo_pdf.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{archivo_pdf.name}"'

    return response


def mostrarEstudioMedico(request, id_Estudio):
    estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    return render(request, 'estudioMedico.html', {'estudio': estudio})

def mostrarRadiografiaMedico(request, id_Radiografia):
    radiografia = get_object_or_404(Radiografias, id_Radiografia=id_Radiografia)
    return render(request, 'radiografiaMedico.html', {'radiografia': radiografia})

def mostrarEstudioEnfermero(request, id_Estudio, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    return render(request, 'estudioEnfermero.html', {'estudio': estudio, "paciente": paciente})

def mostrarRadiografiaEnfermero(request, id_Radiografia, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    radiografia = get_object_or_404(Radiografias, id_Radiografia=id_Radiografia)
    return render(request, 'radiografiaEnfermero.html', {'radiografia': radiografia, "paciente": paciente})

def listaTratamientosEnfermero(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientos = Tratamiento.objects.filter(paciente=expediente)
    return render(request, "listaTratamientosEnfermero.html", {'paciente': paciente, 'tratamientos': tratamientos})

def actualizacion_Aplicacion_Tratamiento(request, expediente, id_tratamiento):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamiento = get_object_or_404(Tratamiento, id_Tratamiento=id_tratamiento, paciente=paciente)

    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            # Guardar el tratamiento actualizado
            tratamiento_actualizado = form.save()

            # Registrar el historial de aplicación
            HistorialAplicacion.objects.create(
                tratamiento=tratamiento_actualizado,
                fecha_aplicacion=timezone.now()
            )

            messages.success(request, "Tratamiento editado y aplicación registrada con éxito.")
            return redirect('perfilPacienteEnfermero', expediente=paciente.expediente)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = TratamientoForm(instance=tratamiento)

    # Renderizar el formulario
    return render(request, 'actualizacion_Aplicacion_Tratamiento.html', {
        'form': form,
        'paciente': paciente,
        'tratamiento': tratamiento
    })

def historial_aplicacion_por_paciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    historial = HistorialAplicacion.objects.filter(tratamiento__paciente=paciente).order_by('-fecha_aplicacion')

    return render(request, 'historial_aplicacion_paciente.html', {
        'paciente': paciente,
        'historial': historial
    })


def historial_aplicacion_por_tratamiento(request, id_tratamiento):
    tratamiento = get_object_or_404(Tratamiento, id_Tratamiento=id_tratamiento)
    historial = tratamiento.historiales.all().order_by('-fecha_aplicacion')  # Ordenar por fecha descendente

    return render(request, 'historialAplicacion.html', {
        'tratamiento': tratamiento,
        'historial': historial
    })

def deshabilitarPaciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    paciente.paciente_Habilitado = "Deshabilitado"
    paciente.save()
    return redirect('mostrarPacientesEnfermero')

def habilitarPaciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    paciente.paciente_Habilitado = "Habilitado"
    paciente.save()
    return redirect("mostrarPacientesEnfermero")

def pacientesDeshabilitados(request):
    pacientes = Paciente.objects.filter(paciente_Habilitado="Deshabilitado")
    return render(request, "pacientesDeshabilitados.html", context={"pacientes" : pacientes})

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
    usuario=request.user.userprofile.funcionalidad
    # Obtener el paciente y el tratamiento asociado
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamiento = get_object_or_404(Tratamiento, id_Tratamiento=id_tratamiento, paciente=paciente)


    if request.method == 'POST':
        # Crear un formulario con los datos enviados
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()  # Guardar cambios en el tratamiento
            messages.success(request, "Tratamiento editado con éxito.")
            if (usuario == 'medico'):
                return redirect('perfilPacienteMedico', expediente=paciente.expediente)
            elif (usuario == 'enfermero'):
                return redirect('perfilPacienteEnfermero', expediente=paciente.expediente)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        # Crear el formulario con la instancia del tratamiento para editar
        form = TratamientoForm(instance=tratamiento)

    return render(request, 'editarTratamiento.html', {'form': form, 'paciente': paciente, 'tratamiento': tratamiento})


# Modificar
def perfilPacienteMedico(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientosActivos = Tratamiento.objects.filter(paciente=expediente)
    tratamientosInactivos = Tratamiento.objects.filter(paciente=expediente)
    radiografias = Radiografias.objects.filter(paciente=expediente)
    estudios = Estudios.objects.filter(paciente=expediente)
    return render(request, "perfilPacienteMedico.html", {'paciente': paciente, 'tratamientosActivos': tratamientosActivos, 'tratamientosInactivos': tratamientosInactivos,
                  'estudios': estudios, 'radiografias': radiografias})


def listaTratamientos(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamientos = Tratamiento.objects.filter(paciente=expediente)
    return render(request, "listaTratamientos.html", {'paciente': paciente, 'tratamientos': tratamientos})

def estudios_GabineteMedico(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)

    estudios = Estudios.objects.filter(paciente=paciente)
    radiografias = Radiografias.objects.filter(paciente=paciente)

    return render(request, 'estudiosyGabineteMedico.html',
                  context={'paciente': paciente, 'estudios': estudios, 'radiografias': radiografias})


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

            # Agregacion de grupos
            grupo_nombre = profile.funcionalidad
            grupo = Group.objects.filter(name=grupo_nombre).first()

            if grupo:
                user.groups.add(grupo)
                messages.success(self.request, f"Usuario registrado y asigndo al grupo {grupo_nombre}.")
            else:
                messages.warning(self.request, f"Usuario registrado, pero no se encontró un grupo.")
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

def edicionUsuario(request, id):
    # Obtener el usuario y perfil asociados, o mostrar un 404 si no se encuentran
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        # Cargar el formulario con los datos enviados y las instancias actuales
        user_form = RegisterForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        # Guardar los formularios si son válidos
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save(commit=True)
            profile_form.save(commit=True)
            messages.success(request, "Usuario actualizado con éxito.")
            return redirect('perfilUsuario', id=user.id)
        else:
            messages.error(request, "Hubo un error al actualizar el usuario.")
    else:
        # Inicializar los formularios con los datos actuales del usuario y perfil
        user_form = RegisterForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    # Renderizar la página con los formularios y datos actuales
    return render(request, 'editarUsuario.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_data': user,
        'profile_data': user_profile
    })

def deshabilitar_Usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()
    messages.success(request,"El usuario fue deshabilitado correctamente.")
    return redirect('usuarios')


def habilitar_Usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    messages.success(request, "El usuario fue habilitado correctamente.")
    return redirect("usuarios")


def perfilUsuario(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    if (user.is_active):
        return render(request, "perfilUsuario.html", {'user': user, 'user_profile': user_profile})
    else:
        return render(request, "perfilUsuarioDeshabilitado.html", {'user': user, 'user_profile': user_profile})


def usuarios(request):
    users = User.objects.select_related('user_profile').all()
    return render(request, "usuarios.html", {'users': users})

def mostrarUsuarios(request):
    users = User.objects.filter(is_active=True)
    return render(request, "usuarios.html", {"users": users})

def mostrarUsuariosDeshabilitados(request):
    users = User.objects.filter(is_active=False)
    return render(request, "usuariosDeshabilitados.html", context={"users": users})

def usuariosDeshabilitados(request):
    users = User.objects.select_related('user_profile').filter(is_active=False)
    return render(request, "usuariosDeshabilitados.html", {'users': users})



# --------------------------------------------| INTERFACES DE VISTA GENERAL |--------------------------------------------

def signosVitales(request):
    return HttpResponse(render(request, "signosVitales.html"))



# --------------------------------------------| INTERFACES DE MUESTRA DE DATOS |--------------------------------------------

def mostrarPacientesEnfermero(request):
    pacientes = Paciente.objects.filter(paciente_Habilitado="Habilitado")
    return render(request, 'pacientesEnfermero.html', {'Pacientes': pacientes})

def mostrarPacientesDeshabilitados(request):
    pacientes = Paciente.objects.filter(paciente_Habilitado="Deshabilitado")
    return render(request, 'pacientesDeshabilitados.html', {'Pacientes': pacientes})

def mostrarPacientesMedico(request):
    pacientes = Paciente.objects.filter(medico_Encargado__user=request.user, paciente_Habilitado="Habilitado")
    return render(request, 'pacientesMedico.html', {'Pacientes': pacientes})

