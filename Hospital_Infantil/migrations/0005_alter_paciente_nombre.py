# Generated by Django 5.1.2 on 2024-11-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital_Infantil', '0004_remove_paciente_altura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
