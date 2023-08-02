# Generated by Django 4.2.1 on 2023-08-02 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('g_Deportiva', '0005_alter_people_allergies_alter_people_disabilities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='allergies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.allergies'),
        ),
        migrations.AlterField(
            model_name='people',
            name='disabilities',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.disabilities'),
        ),
    ]
