from django.contrib import admin
from .models import Paciente, Tratamiento, UserProfile

admin.site.register(Paciente)
admin.site.register(Tratamiento)
admin.site.register(UserProfile)