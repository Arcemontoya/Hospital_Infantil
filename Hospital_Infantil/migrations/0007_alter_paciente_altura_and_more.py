# Generated by Django 5.1.2 on 2024-11-02 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0006_paciente_altura_paciente_apellido_materno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='altura',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='apellido_materno',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='apellido_paterno',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cirugia_realizada',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='diagnostico_clinico_prequirurgico',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nota_enfermeria',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='peso',
            field=models.FloatField(default=0.0),
        ),
    ]