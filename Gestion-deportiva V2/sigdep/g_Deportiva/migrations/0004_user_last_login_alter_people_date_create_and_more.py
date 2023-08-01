# Generated by Django 4.2.1 on 2023-08-01 15:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('g_Deportiva', '0003_remove_programmingtournaments_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='date_create',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='g_Deportiva.people'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='g_Deportiva.rol'),
        ),
    ]
