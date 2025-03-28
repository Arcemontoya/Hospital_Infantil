import profile
from itertools import chain

from django.contrib.auth.forms import AuthenticationForm
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView, ListView, DetailView
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from .forms import EditUserForm, RegisterForm, PacienteForm, UserProfileForm, TratamientoForm, EstudiosForm, RadiografiasForm, \
    SuministroTratamiento
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from django.utils import timezone

from .models import Paciente, UserProfile, Tratamiento, Radiografias, Estudios, HistorialAplicacion

import logging
from django.contrib.messages import get_messages
from django.core.mail import send_mail
import random
from django.conf import settings
from django.views.decorators.http import require_POST
import os

def index(request):
    return render(request, 'index.html')

# --------------------------------------------| LOGIN |--------------------------------------------
logger = logging.getLogger(__name__)
class CustomLoginView(View):
    def get(self, request):
        # Guardar la URL de referencia en la sesión si no viene de un error
        if 'prev_page' not in request.session or request.META.get('HTTP_REFERER') != request.build_absolute_uri():
            request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')

        # Limpia los mensajes pendientes
        storage = get_messages(request)
        for _ in storage:
            pass

        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        logger.info("Ingresando al login")
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)

                # Verifica si hay un 'next' en la URL para redirigir
                next_url = request.GET.get('next')
                if (next_url):
                    return redirect(next_url)

                # Redirige según el rol del usuario
                user_profile = UserProfile.objects.get(user=user)
                role = user_profile.funcionalidad
                if role == 'administrador':
                    return redirect('usuarios')
                elif role in ['medico', 'enfermero']:
                    return redirect('pacientes')
            else:
                form.add_error(None, "Nombre de usuario o contraseña incorrectos.")
        else:
            logger.info("Usuario o contraseña incorrectos.")
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")

        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --------------------------------------------| VISTA DE ADMINISTRADOR |--------------------------------------------
class RegistroUsuario(FormView):
    template_name = 'registroUsuario.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        """ Guarda la URL de referencia al acceder a la vista """
        if 'prev_page' not in request.session or not request.session['prev_page']:
            request.session['prev_page'] = request.META.get('HTTP_REFERER', reverse_lazy('usuarios'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """ Usa la URL guardada en la sesión y la limpia después de usarla """
        return self.request.session.pop('prev_page', reverse_lazy('usuarios'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'profile_form' not in context:
            context['profile_form'] = UserProfileForm()

        # Consumir mensajes para que se eliminen después de mostrarlos
        storage = get_messages(self.request)
        context['messages'] = list(storage)  # Pasar los mensajes al contexto y vaciarlos
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        profile_form = UserProfileForm(request.POST)

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

            grupo_nombre = profile.funcionalidad
            grupo = Group.objects.filter(name=grupo_nombre).first()
            if grupo:
                user.groups.add(grupo)
                messages.success(self.request, f"Usuario registrado y asignado al grupo {grupo_nombre}.")
            else:
                messages.warning(self.request, f"Usuario registrado, pero no se encontró un grupo.")

            messages.success(self.request, "Usuario registrado con éxito.")
            return HttpResponseRedirect(self.get_success_url())  # Redirige a la página original
        except Exception as e:
            messages.error(self.request, f"Error al registrar el usuario: {e}")
            return self.form_invalid(form, profile_form)

    def form_invalid(self, form, profile_form):
        # Diccionario de nombres personalizados para los campos
        field_labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña',
            'fecha_registro': 'Fecha de ingreso',
            'cedula_profesional': 'Cédula profesional',
            'funcionalidad': 'Rol del usuario'
        }

        error_messages = []
        for field, errors in form.errors.items():
            field_name = field_labels.get(field, field)  # Usa el nombre personalizado si está en el diccionario
            for error in errors:
                error_messages.append(f"{field_name}:\n {_(error)}")

        for field, errors in profile_form.errors.items():
            field_name = field_labels.get(field, field)
            for error in errors:
                error_messages.append(f"{field_name}: {_(error)}")

        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form, error_messages="\n".join(error_messages))
        )

# Refactorizar
def edicionUsuario(request, id):
    # Obtener el usuario y su perfil, o lanzar un 404 si no existen
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        # Formulario con los datos enviados y las instancias actuales
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save(commit=True)
                profile_form.save(commit=True)
                messages.success(request, "✅ Usuario actualizado con éxito.")
                return redirect('perfilUsuario', id=user.id)
            except Exception as e:
                messages.error(request, f"❌ Error al actualizar el usuario: {e}")
        else:
            # Agregar errores específicos a los mensajes
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {user_form.fields[field].label}: {error}")
            
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {profile_form.fields[field].label}: {error}")

            messages.error(request, "⚠️ Hubo errores en el formulario. Por favor, revisa los campos.")

    else:
        # Inicializar los formularios con datos actuales
        user_form = RegisterForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    # Renderizar la plantilla con los formularios y los mensajes
    response = render(request, 'editarUsuario.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_data': user,
        'profile_data': user_profile
    })

    # Limpiar mensajes de error después de mostrarlos
    storage = messages.get_messages(request)
    storage.used = True

    return response

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
    
def agregar_enfermero(request):
    form = PacienteForm()
    form_html = render_to_string('partials/enfermero_form.html', {'form': form}, request=request)
    return HttpResponse(form_html)

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



# --------------------------------------------| RECUPERACION DE CUENTA |--------------------------------------------
def recuperarCuenta(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            codigo = str(random.randint(100000, 999999))
            request.session["codigo_recuperacion"] = codigo
            request.session["email_recuperacion"] = email
            send_mail(
                subject="Código de Recuperación de Cuenta",
                message=f"Tu código de recuperación es: {codigo}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect("verificarCodigo")

        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")

    return render(request, "recuperacionCuenta.html")


def verificarCodigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get("codigo")
        codigo_guardado = request.session.get("codigo_recuperacion")

        if codigo_ingresado == codigo_guardado:
            return redirect("cambiarPassword")
        else:
            messages.error(request, "Código incorrecto. Inténtalo de nuevo.")

    return render(request, "verificarCodigo.html")


def cambiarPassword(request):
    if request.method == "POST":
        nueva_contraseña = request.POST.get("password")
        confirmar_contraseña = request.POST.get("confirm_password")
        email = request.session.get("email_recuperacion")

        if not email:
            messages.error(request, "Ocurrió un error. Vuelve a solicitar la recuperación de contraseña.")
            return redirect("recuperarCuenta")

        if nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("cambiarPassword")

        try:
            usuario = User.objects.get(email=email)
            usuario.set_password(nueva_contraseña)
            usuario.save()
            messages.success(request, "Contraseña cambiada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            return redirect("recuperarCuenta")

    return render(request, "cambiarPassword.html")

@require_POST
def delete_pdfEstudios(request, id_Estudio):
    try:
        estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
        # Delete the file from storage
        if estudio.estudio:
            if os.path.isfile(estudio.estudio.path):
                os.remove(estudio.estudio.path)
        estudio.estudio = None
        estudio.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def replace_pdfEstudios(request, id_Estudio):
    try:
        estudio = get_object_or_404(Estudios, id_Estudio=id_Estudio)
        if 'estudio' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No se proporcionó ningún archivo'})
        
        new_file = request.FILES['estudio']
        if not new_file.name.endswith('.pdf'):
            return JsonResponse({'success': False, 'error': 'El archivo debe ser un PDF'})
        
        # Delete old file if it exists
        if estudio.estudio:
            if os.path.isfile(estudio.estudio.path):
                os.remove(estudio.estudio.path)
        
        # Save new file
        estudio.estudio = new_file
        estudio.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})