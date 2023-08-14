# Generated by Django 4.2.1 on 2023-08-01 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergie_name', models.CharField(max_length=45)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_technicalv', models.CharField(max_length=50)),
                ('at_tacticalv', models.CharField(max_length=50)),
                ('at_physicalv', models.CharField(max_length=50)),
                ('athlete_status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Disabilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disability_name', models.CharField(max_length=45)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('experience_years', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=230)),
                ('photo_user', models.ImageField(upload_to='media/')),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(max_length=9)),
                ('telephone_number', models.CharField(max_length=10)),
                ('date_create', models.DateField()),
                ('type_document_id', models.CharField(max_length=20)),
                ('num_document', models.IntegerField()),
                ('file_documentidentity', models.FileField(upload_to='documents/')),
                ('file_v', models.FileField(upload_to='documents/')),
                ('file_f', models.FileField(upload_to='documents/')),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('is_instructors', models.BooleanField()),
                ('allergies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.allergies')),
                ('disabilities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.disabilities')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_rol', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=40)),
                ('service_status', models.IntegerField()),
                ('description', models.TextField()),
                ('service_value', models.DecimalField(decimal_places=0, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sport_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=40)),
                ('team_image', models.CharField(max_length=255)),
                ('date_create_team', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=250)),
                ('instructors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.instructors')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.sports')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('password', models.CharField(max_length=128)),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.people')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.rol')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Tournaments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_tournament', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('max_teams', models.IntegerField()),
                ('max_participants_ethlete', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('prize', models.CharField(max_length=100)),
                ('registration_fee', models.DecimalField(decimal_places=0, max_digits=10)),
                ('enrollment_status', models.BooleanField(default=True)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.athlete')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.team')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_day', models.DateField()),
                ('full_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('r_athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.athlete')),
                ('r_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.services')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingTournaments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('position', models.IntegerField()),
                ('matches_played', models.IntegerField()),
                ('win', models.IntegerField()),
                ('lose', models.IntegerField()),
                ('tie', models.IntegerField(db_column='Tie')),
                ('penalty_score', models.IntegerField()),
                ('registration_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.tournaments')),
            ],
        ),
        migrations.AddField(
            model_name='instructors',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.people'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(max_length=11)),
                ('c_name', models.CharField(max_length=30)),
                ('date_create_category', models.DateTimeField(auto_now_add=True)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.sports')),
            ],
        ),
        migrations.CreateModel(
            name='AthleteTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dorsal', models.IntegerField()),
                ('positions_initial', models.CharField(max_length=45)),
                ('position_alternative', models.CharField(max_length=45)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.athlete')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.team')),
            ],
        ),
        migrations.AddField(
            model_name='athlete',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.instructors'),
        ),
        migrations.AddField(
            model_name='athlete',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.people'),
        ),
        migrations.AddField(
            model_name='athlete',
            name='sports',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.sports'),
        ),
        migrations.CreateModel(
            name='Anthropometric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controlDate', models.DateField()),
                ('arm', models.IntegerField()),
                ('chest', models.CharField(max_length=45)),
                ('hip', models.IntegerField()),
                ('twin', models.IntegerField()),
                ('humerus', models.IntegerField()),
                ('femur', models.IntegerField()),
                ('wrist', models.IntegerField()),
                ('triceps', models.IntegerField()),
                ('supraspinal', models.IntegerField()),
                ('pectoral', models.IntegerField()),
                ('zise', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('bmi', models.IntegerField()),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_Deportiva.athlete')),
            ],
        ),
    ]
