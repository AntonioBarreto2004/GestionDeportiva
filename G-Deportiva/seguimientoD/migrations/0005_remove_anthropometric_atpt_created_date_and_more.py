# Generated by Django 4.2.1 on 2023-07-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguimientoD', '0004_alter_anthropometric_atpt_updated_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anthropometric',
            name='atpt_created_date',
        ),
        migrations.AlterField(
            model_name='anthropometric',
            name='atpt_controlDate',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de Control'),
        ),
        migrations.AlterField(
            model_name='anthropometric',
            name='atpt_updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
