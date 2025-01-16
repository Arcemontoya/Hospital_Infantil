from django.apps import AppConfig
from django.db.models.signals import post_migrate


def crear_grupos(sender, **kwargs):
    from django.contrib.auth.models import Group  # Importación retrasada
    grupos = ['administrador', 'medico', 'enfermero']
    for nombre in grupos:
        Group.objects.get_or_create(name=nombre)

class HospitalInfantilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "Hospital_Infantil"

    def ready(self):
        post_migrate.connect(crear_grupos, sender=self)