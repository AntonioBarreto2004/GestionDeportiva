# Generated by Django 4.2.1 on 2023-06-07 19:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_name', models.CharField(max_length=30, verbose_name='Tipo de deporte')),
                ('c_name', models.CharField(max_length=30, verbose_name='Nombre Categoría')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_position', models.CharField(max_length=50, verbose_name='Posición Principal')),
                ('at_positiona', models.CharField(max_length=50, verbose_name='Posición Alternativa')),
            ],
            options={
                'verbose_name': 'Posición',
                'verbose_name_plural': 'Posiciones',
                'db_table': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=40, verbose_name='Nombre de equipo')),
                ('team_image', models.ImageField(upload_to='media/', verbose_name='Foto del Equipo')),
                ('team_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimientoD.category', verbose_name='Categoría')),
                ('team_user', models.ManyToManyField(limit_choices_to={'profile__cod_rol__name_rol': 'Instructor'}, to=settings.AUTH_USER_MODEL, verbose_name='Instructor')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dorsal', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Dorsal Jugador')),
                ('at_technicalv', models.CharField(max_length=50, verbose_name='Valoración Técnica')),
                ('at_tacticalv', models.CharField(max_length=50, verbose_name='Valoración Táctica')),
                ('at_physicalv', models.CharField(max_length=50, verbose_name='Valoración Física')),
                ('a_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimientoD.category', verbose_name='Deporte')),
                ('at_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimientoD.team', verbose_name='Equipo')),
                ('at_user', models.ManyToManyField(limit_choices_to={'profile__cod_rol__name_rol': 'Atleta'}, to=settings.AUTH_USER_MODEL, verbose_name='Atleta')),
                ('c_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posicion_inicial', to='seguimientoD.positions', verbose_name='Posición Principal')),
                ('c_positiona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posicion_alterna', to='seguimientoD.positions', verbose_name='Posición Alterna')),
            ],
            options={
                'verbose_name': 'Atleta',
                'verbose_name_plural': 'Atletas',
                'db_table': 'athlete',
            },
        ),
        migrations.CreateModel(
            name='Anthropometric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atpt_controlDate', models.DateField(verbose_name='Fecha de Control')),
                ('atpt_arm', models.IntegerField(verbose_name='Brazo')),
                ('atpt_chest', models.CharField(max_length=45, verbose_name='Pecho')),
                ('atpt_hip', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Cadera')),
                ('atpt_calf', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Gemelo')),
                ('atpt_humerus', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Húmero')),
                ('atpt_femur', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Fémur')),
                ('atpt_wrist', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Muñeca')),
                ('atpt_triceps', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Tríceps')),
                ('atpt_suprailiac', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Supraespinal')),
                ('atpt_pectoral', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Pectoral')),
                ('atpt_height', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Talla')),
                ('atpt_weight', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Peso')),
                ('atpt_bmi', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='IMC')),
                ('atpt_created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('atpt_updated_date', models.DateField(auto_now=True, verbose_name='Fecha Actualización')),
                ('athlete_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimientoD.athlete', verbose_name='Atleta')),
            ],
            options={
                'verbose_name': 'Antropométrica',
                'verbose_name_plural': 'Antropométricas',
                'db_table': 'anthropometric',
            },
        ),
    ]
