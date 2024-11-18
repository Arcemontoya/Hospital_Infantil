from datetime import date

import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models
from django import utils
from django.utils import timezone

class UserProfile(models.Model):

    FUNCIONALIDAD_CHOICES = [
        ('administrador', 'ADMINISTRADOR'),
        ('medico', 'MEDICO'),
        ('enfermero', 'ENFERMERO')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_registro = models.DateField(blank=True, null=True)
    cedula_profesional = models.DecimalField(max_digits=8, decimal_places=0, blank=True)
    funcionalidad = models.CharField(
        max_length=20,
        choices=FUNCIONALIDAD_CHOICES
    )

    def __str__(self):
        return self.user.username


# ------------------------------------------ |PACIENTE| ------------------------------------------------------------
class Paciente(models.Model):
    expediente = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=50, blank=False)

    apellido_paterno = models.CharField(max_length=50, blank=False)
    apellido_materno = models.CharField(max_length=50, blank=False)
    fecha_ingreso = models.DateField(default=timezone.now)
    fecha_nacimiento = models.DateField(default=timezone.now)
    cirugia_realizada = models.CharField(max_length=100, blank=False)
    peso = models.FloatField(blank=False, default=0.0)
    altura = models.FloatField(blank=False, default=0.0)
    diagnostico_clinico_prequirurgico = models.CharField(max_length=1000, blank=False)
    nota_enfermeria = models.CharField(max_length=1000, blank=False)
    medico_Encargado = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null = True,
        limit_choices_to={'user__userprofile__funcionalidad': 'medico'},
    )


    def __str__(self):
        return self.nombre


# ------------------------------------------ |TRATAMIENTO| ------------------------------------------------------------

class Tratamiento(models.Model):
    TIEMPO_DOSIS_CHOICES = [
        ('hrs', 'HRS'),
        ('mins', 'MINS'),
        ('unica', 'UNICA'),
        ('prn', 'PRN')
    ]

    VIA_ADMINISTRACION_CHOICES = [
        ('cutanea','CUTANEA'),
        ('inhalada', 'INHALADA'),
        ('intradermica', 'INTRADERMICA'),
        ('im_intramuscular', 'IM-INTRAMUSCULAR'),
        ('iv_intravenosa', 'IV-INTRAVENOSA'),
        ('nasal', 'NASAL'),
        ('oftalmica', 'OFTALMICA'),
        ('oral', 'ORAL'),
        ('otica', 'OTICA'),
        ('rectal', 'RECTAL'),
        ('sonda_nasogastrica', 'SONDA NASOGASTRICA'),
        ('subcutanea', 'SUBCUTANEA'),
        ('sublingual', 'SUBLINGUAL'),
        ('topica', 'TOPICA'),
        ('vaginal', 'VAGINAL'),
    ]

    id_Tratamiento = models.AutoField(primary_key=True, unique=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='tratamientos', null=True)
    nombre_Medicamento = models.CharField(max_length=50)
    dosis_Administrada = models.FloatField()
    via_Administracion = models.CharField(
        max_length=20,
        choices=VIA_ADMINISTRACION_CHOICES
    )
    frecuencia_Dosis = models.DecimalField(max_digits=2, decimal_places=0)
    tiempo_Dosis = models.CharField(
        max_length= 10,
        choices=TIEMPO_DOSIS_CHOICES
    )
    duracion_Terapia = models.DecimalField(max_digits=2, decimal_places=0)
    otras_Indicaciones = models.CharField(max_length=1000, null=True)

class Estudios(models.Model):
    id_Estudio = models.AutoField(primary_key=True, unique=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='estudios', null=True)
    nombre_Estudio = models.CharField(max_length=20, null=False)
    fecha_realizada = models.DateField(default=timezone.now)
    estudio = models.FileField(upload_to='estudios/')


class Radiografias(models.Model):
    id_Radiografia = models.AutoField(primary_key=True, unique=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='radiografias', null=True)
    nombre_Radiografia = models.CharField(max_length=20, null=False)
    fecha_realizada = models.DateField(default=timezone.now)
    radiografia = models.FileField(upload_to='radiografias/')

