# Generated by Django 4.2.1 on 2023-08-04 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g_Deportiva', '0010_alter_people_is_instructors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anthropometric',
            name='controlDate',
            field=models.DateField(auto_now_add=True),
        ),
    ]