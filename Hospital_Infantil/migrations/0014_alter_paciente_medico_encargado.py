# Generated by Django 5.1.2 on 2024-11-07 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0013_remove_paciente_otras_indicaciones_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='medico_Encargado',
            field=models.ForeignKey(limit_choices_to={'user__userprofile__funcionalidad': 'medico'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
