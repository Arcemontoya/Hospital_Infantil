from django.contrib.auth.models import User
from django.db import models

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_registro = models.DateField(blank=True, null=True)
    cedula_profesional = models.DecimalField(max_digits=8, decimal_places=0, blank=True)
"""

# ------------------------------------------ |PACIENTE| ------------------------------------------------------------
class Paciente(models.Model):
    expediente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    apellido_paterno = models.CharField(max_length=50, blank=True)
    apellido_materno = models.CharField(max_length=50, blank=True)
    fecha_ingreso = models.DateField()
    fecha_nacimiento = models.DateField()
    cirugia_realizada = models.CharField(max_length=100, blank=True)
    peso = models.FloatField()
    altura = models.FloatField()
    diagnostico_clinico_prequirurgico = models.CharField(max_length=1000, blank=True)
    nota_enfermeria = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.nombre

# ------------------------------------------ |TRATAMIENTO| ------------------------------------------------------------
