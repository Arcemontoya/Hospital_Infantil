import profile
import os
import json
from itertools import chain

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView, ListView, DetailView

from .forms import RegisterForm, PacienteForm, UserProfileForm, TratamientoForm, EstudiosForm, RadiografiasForm, \
    SuministroTratamiento
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from django.utils import timezone
from django.template.loader import render_to_string

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
                elif role == 'medico' or role == 'enfermero':
                    return redirect('pacientes')  # Vista de medico y enfermero
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --------------------------------------------| VISTA DE ADMINISTRADOR |--------------------------------------------

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

# Refactorizar
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

# Refactorizar
def deshabilitar_Usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()
    messages.success(request,"El usuario fue deshabilitado correctamente.")
    return redirect('usuarios')

# Refactorizar
def habilitar_Usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()
    messages.success(request, "El usuario fue habilitado correctamente.")
    return redirect("usuarios")


# Refactorizar
def perfilUsuario(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    if (user.is_active):
        return render(request, "perfilUsuario.html", {'user': user, 'user_profile': user_profile})
    else:
        return render(request, "perfilUsuarioDeshabilitado.html", {'user': user, 'user_profile': user_profile})


# Refactorizar
def usuarios(request):
    users = User.objects.select_related('user_profile').all()
    return render(request, "usuarios.html", {'users': users})

# Refactorizar
def mostrarUsuarios(request):
    users = User.objects.filter(is_active=True)
    return render(request, "usuarios.html", {"users": users})

# Refactorizar
def mostrarUsuariosDeshabilitados(request):
    users = User.objects.filter(is_active=False)
    return render(request, "usuariosDeshabilitados.html", context={"users": users})

# Refactorizar
def usuariosDeshabilitados(request):
    users = User.objects.select_related('userprofile').filter(is_active=False)
    return render(request, "usuariosDeshabilitados.html", {'users': users})


# --------------------------------------------| DESPLIEGUE DE PACIENTES |--------------------------------------------

class desplieguePacientesHabilitados(ListView):
    template_name = "Patients/pacientes.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        print(f"Usuario: {self.request.user}, Funcionalidad: {user_profile.funcionalidad}")

        if user_profile.funcionalidad == "medico":
            pacientes = Paciente.objects.filter(medico_Encargado=user_profile, paciente_Habilitado="Habilitado")
        elif user_profile.funcionalidad == "enfermero":
            pacientes = Paciente.objects.filter(enfermeros_Encargados=user_profile, paciente_Habilitado="Habilitado")
        else:
            pacientes = Paciente.objects.all()

        print(f"Pacientes encontrados: {pacientes.count()} -> {list(pacientes)}")  # Imprime los pacientes
        return pacientes


class desplieguePacientesDeshabilitados(ListView):
    template_name = "pacientesDeshabilitados.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        return Paciente.objects.filter(paciente_Habilitado="Deshabilitado")


# --------------------------------------------| REGISTRO DE PACIENTES |--------------------------------------------
# Funciona no implementado URL
class RegistroPaciente(FormView):
    template_name = 'registroPaciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('pacientes')

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

# --------------------------------------------| EDICION DE PACIENTES |--------------------------------------------
class edicionPacientes(UpdateView):
    model = Paciente
    template_name = "editarPaciente.html"
    form_class = PacienteForm
    slug_field = "expediente"
    slug_url_kwarg = "expediente"

    def get_object(self):
        expediente = self.kwargs.get('expediente')
        return get_object_or_404(Paciente, expediente=expediente)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Paciente editado con éxito.")
        expediente = self.kwargs.get('expediente')
        paciente = Paciente.objects.get(expediente=expediente)
        return redirect(reverse('perfilPaciente', kwargs={'pk': paciente.expediente}))

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)



# --------------------------------------------| PERFIL DE PACIENTES |--------------------------------------------

class perfilPaciente(DetailView):
    model = Paciente
    template_name = 'Patients/perfilPaciente.html'
    context_object_name = "paciente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamientos_activos'] = Tratamiento.objects.filter(paciente_id = self.object, tratamiento_activo='activo').prefetch_related("historiales")
        context['tratamientos_inactivos'] = Tratamiento.objects.filter(paciente_id = self.object, tratamiento_activo='Inactivo').prefetch_related("historiales")
        return context


# --------------------------------------------| REGISTRO DE ESTUDIOS |--------------------------------------------
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

        self.success_url = reverse('estudiosyGabinete', args=[expediente])
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)

def agregar_enfermero(request):
    form = PacienteForm()
    form_html = render_to_string('partials/enfermero_form.html', {'form': form}, request=request)
    return HttpResponse(form_html)

# --------------------------------------------| REGISTRO DE RADIOGRAFIAS |--------------------------------------------

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

        self.success_url = reverse('estudiosyGabinete', args=[expediente])
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)

# --------------------------------------------| MOSTRAR ESTUDIOS Y GABINETE |--------------------------------------------
class EstudiosYGabinete(ListView):
    template_name = "estudiosyGabinete.html"
    context_object_name = "estudiosyGabinete"

    def get_queryset(self):
        paciente_id = self.kwargs.get('expediente')
        estudios = Estudios.objects.filter(paciente_id=paciente_id)
        radiografias = Radiografias.objects.filter(paciente_id=paciente_id)
        return list(chain(estudios, radiografias))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_expediente  = self.kwargs.get('expediente')
        context["paciente"] = get_object_or_404(Paciente, expediente=paciente_expediente)
        return context


# No mover
def ver_pdfEstudios(request, id_Estudio):
    estudios = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    archivo_pdf = estudios.estudio
    response = FileResponse(archivo_pdf.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{archivo_pdf.name}"'

    return response

# No mover
def ver_pdfRadiografias(request, id_Radiografia):
    radiografia = get_object_or_404(Radiografias, id_Radiografia=id_Radiografia)
    archivo_pdf = radiografia.radiografia
    response = FileResponse(archivo_pdf.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{archivo_pdf.name}"'

    return response

def mostrarEstudios(request, expediente, id_Estudio):
    paciente = get_object_or_404(Paciente, expediente = expediente)
    estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    return render(request, 'Studies and X-Rays/estudios.html', {'estudio': estudio, "paciente": paciente})

def mostrarRadiografias(request, expediente, id_Radiografia):
    paciente = get_object_or_404(Paciente, expediente = expediente)
    radiografia = get_object_or_404(Radiografias, id_Radiografia=id_Radiografia)
    return render(request, 'Studies and X-Rays/radiografias.html', {'radiografia': radiografia, "paciente": paciente})

# Función para reemplazar un estudio
def reemplazar_estudio(request, id_Estudio):
    if request.method == 'POST':
        estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
        paciente = estudio.paciente
        
        # Verificar si se proporcionó un nuevo archivo
        if 'nuevo_archivo' in request.FILES:
            # Eliminar el archivo anterior si existe
            if estudio.estudio:
                if os.path.isfile(estudio.estudio.path):
                    os.remove(estudio.estudio.path)
            
            # Guardar el nuevo archivo
            estudio.estudio = request.FILES['nuevo_archivo']
            estudio.save()
            
            messages.success(request, 'El estudio ha sido reemplazado correctamente.')
        else:
            messages.error(request, 'No se proporcionó un archivo para reemplazar el estudio.')
        
        return redirect('estudio', expediente=paciente.expediente, id_Estudio=id_Estudio)
    
    # Si no es POST, redirigir a la página del estudio
    return redirect('estudio', expediente=estudio.paciente.expediente, id_Estudio=id_Estudio)

# Función para eliminar un estudio
def eliminar_estudio(request, id_Estudio, expediente):
    estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
    paciente = estudio.paciente
    
    # Eliminar el archivo físico si existe
    if estudio.estudio:
        if os.path.isfile(estudio.estudio.path):
            os.remove(estudio.estudio.path)
    
    # Eliminar el registro de la base de datos
    estudio.delete()
    
    messages.success(request, 'El estudio ha sido eliminado correctamente.')
    
    # Redirigir a la página de estudios y gabinete
    return redirect('estudiosyGabinete', expediente=expediente)

# Refactorizar (Aplicalo dentro de la interfaz)
def actualizacion_Aplicacion_Tratamiento(request, expediente, id_tratamiento):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    tratamiento = get_object_or_404(Tratamiento, id_Tratamiento=id_tratamiento, paciente=paciente)

    if request.method == "POST":
        print(f"Tratamiento antes de la actualización: {tratamiento.tratamiento_activo}")

        HistorialAplicacion.objects.create(tratamiento=tratamiento, fecha_aplicacion=timezone.now())

        # Actualizar el tratamiento
        tratamiento.save()

        print(f"Tratamiento después de la actualización: {tratamiento.tratamiento_activo}")

        return redirect(request.META.get('HTTP_REFERER', 'pacientes'))

    return redirect('pacientes')

# Edición de Historial de Suministrologout_view
class edicionHistorialSuministro(UpdateView):
    model = HistorialAplicacion
    template_name = "edicion_Suministro_Tratamiento.html"
    form_class = SuministroTratamiento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tratamiento"] = self.object.tratamiento
        context["historial_aplicaciones"] = HistorialAplicacion.objects.filter(tratamiento=self.object.tratamiento)
        return context

# Forma parte de edicionHistorialSuministro
@csrf_exempt
def actualizar_historial(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        historial = get_object_or_404(HistorialAplicacion, id=id)
        historial.fecha_aplicacion = data.get("fecha_aplicacion")
        historial.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


# No mover
def deshabilitarPaciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    paciente.paciente_Habilitado = "Deshabilitado"
    paciente.save()
    return redirect('pacientes')

# No mover
def habilitarPaciente(request, expediente):
    paciente = get_object_or_404(Paciente, expediente=expediente)
    paciente.paciente_Habilitado = "Habilitado"
    paciente.save()
    return redirect("pacientes")


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
        paciente = get_object_or_404(Paciente, expediente=self.kwargs.get('expediente'))
        return reverse_lazy('perfilPaciente', kwargs={'pk': paciente.pk})

# --------------------------------------------| EDICION DE TRATAMIENTO |--------------------------------------------
class edicionTratamientos(UpdateView):
    model = Tratamiento
    template_name = "editarTratamiento.html"
    form_class = TratamientoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.kwargs.get('expediente')
        paciente = get_object_or_404(Paciente, expediente=expediente) if expediente else None
        context['expediente'] = expediente
        context['paciente'] = paciente
        return context


    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Tratamiento editado con éxito.")
        expediente = self.kwargs.get('expediente')
        paciente = Paciente.objects.get(expediente=expediente)
        return redirect(reverse('perfilPaciente', kwargs={'pk': paciente.pk}))

    def form_invalid(self, form):
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error en el campo '{field}': {error}")
        return super().form_invalid(form)


# --------------------------------------------| INTERFACES DE VISTA GENERAL |--------------------------------------------

# Pendiente
def signosVitales(request):
    return HttpResponse(render(request, "signosVitales.html"))




