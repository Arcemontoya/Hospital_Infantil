# Generated by Django 5.1.2 on 2024-11-07 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0011_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tratamiento',
            name='otras_Indicaciones',
        ),
        migrations.AddField(
            model_name='paciente',
            name='medico_Encargado',
            field=models.ForeignKey(limit_choices_to={'funcionalidad': 'medico'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hospital_Infantil.userprofile'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='otras_Indicaciones',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]