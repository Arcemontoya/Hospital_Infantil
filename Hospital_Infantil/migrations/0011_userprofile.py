# Generated by Django 5.1.2 on 2024-11-06 21:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0010_tratamiento_paciente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('cedula_profesional', models.DecimalField(blank=True, decimal_places=0, max_digits=8)),
                ('funcionalidad', models.CharField(choices=[('administrador', 'ADMINISTRADOR'), ('medico', 'MEDICO'), ('enfermero', 'ENFERMERO')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]