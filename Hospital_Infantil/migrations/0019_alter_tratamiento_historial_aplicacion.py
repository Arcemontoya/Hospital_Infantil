# Generated by Django 5.1.2 on 2024-12-20 05:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0018_tratamiento_historial_aplicacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamiento',
            name='historial_aplicacion',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
