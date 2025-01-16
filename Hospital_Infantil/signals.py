from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def asignar_grupo_usuario(sender, instance, created, **kwargs):
    if created:  # Solo asignar grupo si el UserProfile es nuevo
        grupo_nombre = instance.funcionalidad
        grupo = Group.objects.filter(name=grupo_nombre).first()
        if grupo:
            instance.user.groups.add(grupo)


class HospitalInfantilConfig(AppConfig):
    default_auto_field = 'django.bd.models.BigAutoField'
    name = "Hospital_Infantil"

    def ready(self):
        import Hospital_Infantil.signals