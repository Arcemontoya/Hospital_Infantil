from django.contrib import admin
from .models import Paciente, Tratamiento, UserProfile, Estudios, Radiografias, HistorialAplicacion, Notificacion

admin.site.register(Paciente)
admin.site.register(Tratamiento)
admin.site.register(UserProfile)
admin.site.register(Estudios)
admin.site.register(Radiografias)
admin.site.register(HistorialAplicacion)
admin.site.register(Notificacion)