# Generated by Django 5.1.2 on 2024-10-31 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('expediente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellido_paterno', models.CharField(blank=True, max_length=50)),
                ('apellido_materno', models.CharField(blank=True, max_length=50)),
                ('fecha_ingreso', models.DateField()),
                ('fecha_nacimiento', models.DateField()),
                ('cirugia_realizada', models.CharField(blank=True, max_length=100)),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('diagnostico_clinico_prequirurgico', models.CharField(blank=True, max_length=1000)),
                ('nota_enfermeria', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]
