# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Allergies(models.Model):
    allergie_name = models.CharField(max_length=45)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'allergies'


class Anthropometric(models.Model):
    athlete = models.ForeignKey('Athlete', models.DO_NOTHING)
    atpt_controldate = models.DateField(auto_now_add=True, db_column='atpt_controlDate')  # Field name made lowercase.
    atpt_arm = models.IntegerField()
    atpt_chest = models.CharField(max_length=45)
    atpt_hip = models.IntegerField()
    atpt_calf = models.IntegerField()
    atpt_humerus = models.IntegerField()
    atpt_femur = models.IntegerField()
    atpt_wrist = models.IntegerField()
    atpt_triceps = models.IntegerField()
    atpt_suprailiac = models.IntegerField()
    atpt_pectoral = models.IntegerField()
    atpt_height = models.IntegerField()
    atpt_weight = models.IntegerField()
    atpt_bmi = models.IntegerField()
    atpt_updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'anthropometric'


class Athlete(models.Model):
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING)
    people = models.ForeignKey('People', models.DO_NOTHING)
    at_technicalv = models.CharField(max_length=50)
    at_tacticalv = models.CharField(max_length=50)
    at_physicalv = models.CharField(max_length=50)
    sports = models.ForeignKey('Sports', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'athlete'


class AthleteTeam(models.Model):
    athlete = models.ForeignKey(Athlete, models.DO_NOTHING)
    team = models.ForeignKey('Team', models.DO_NOTHING)
    dorsal = models.IntegerField()
    positions_initial = models.CharField(max_length=45)
    position_alternative = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'athlete_team'


class Category(models.Model):
    sport = models.ForeignKey('Sports', models.DO_NOTHING)
    category_type = models.CharField(max_length=11)
    c_name = models.CharField(max_length=30)
    date_create_category = models.DateTimeField(auto_now_add=True, db_column='date_create_Category')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class Disabilities(models.Model):
    disability_name = models.CharField(max_length=45)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'disabilities'


class Instructors(models.Model):
    people = models.ForeignKey('People', models.DO_NOTHING)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instructors'


class People(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=230)
    photo_user = models.ImageField(upload_to='media/', null=True, blank=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=9)
    telephone_number = models.CharField(max_length=10)
    date_create = models.DateField(auto_created=True)
    type_document_id = models.CharField(max_length=20)
    num_document = models.IntegerField()
    allergies = models.ForeignKey(Allergies, models.DO_NOTHING, db_column='Allergies_id')  # Field name made lowercase.
    disabilities = models.ForeignKey(Disabilities, models.DO_NOTHING)
    file = models.FileField(upload_to='media/', blank=True)
    file_v = models.FileField(upload_to='media/', blank=True)
    file_f = models.FileField(upload_to='media/', blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_instructors = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'people'


class ProgrammingTournaments(models.Model):
    tournament = models.ForeignKey('Tournaments', models.DO_NOTHING)
    score = models.IntegerField()
    position = models.IntegerField()
    matches_played = models.IntegerField()
    win = models.IntegerField()
    lose = models.IntegerField()
    draw = models.IntegerField()
    penalty_score = models.IntegerField()
    registration_date = models.DateField()
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'programming_tournaments'


class ReceiptPayment(models.Model):
    r_athlete = models.ForeignKey(Athlete, models.DO_NOTHING, db_column='r_athlete')
    r_service = models.ForeignKey('Services', models.DO_NOTHING, db_column='r_service')
    pay_day = models.DateField()
    full_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'receipt_payment'


class Rol(models.Model):
    name_rol = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'rol'


class Services(models.Model):
    service_name = models.CharField(max_length=40)
    service_status = models.IntegerField()
    description = models.TextField()
    service_value = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'services'


class Sports(models.Model):
    sport_name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'sports'


class Team(models.Model):
    team_name = models.CharField(max_length=40)
    sport = models.ForeignKey(Sports, models.DO_NOTHING)
    team_image = models.CharField(max_length=255)
    date_create_team = models.DateTimeField(auto_now_add=True, db_column='date_create_Team')  # Field name made lowercase.
    description = models.CharField(max_length=256)
    instructors = models.ForeignKey(Instructors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team'


class Tournaments(models.Model):
    name_tournament = models.CharField(max_length=100)
    athlete = models.ForeignKey(Athlete, models.DO_NOTHING)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    tournament_type = models.CharField(max_length=10)
    max_teams = models.IntegerField()
    max_participants_per_ethlete = models.IntegerField()
    location = models.CharField(max_length=100)
    prize = models.CharField(max_length=100)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=0)
    enrollment_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tournaments'


class User(models.Model):
    people = models.ForeignKey(People, models.DO_NOTHING)
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'user'
