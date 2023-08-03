from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class Allergies(models.Model):
    allergie_name = models.CharField(max_length=45)
    description = models.TextField()

    def __str__(self):
        return self.allergie_name


class Disabilities(models.Model):
    disability_name = models.CharField(max_length=45)
    description = models.TextField()

    def __str__(self):
        return self.disability_name


class Rol(models.Model):
    name_rol = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name_rol


class People(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=230)
    photo_user = models.ImageField(upload_to='media/', blank=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=9)
    telephone_number = models.CharField(max_length=10)
    date_create = models.DateField(auto_now_add=True)
    type_document_id = models.CharField(max_length=20)
    num_document = models.IntegerField()
    allergies = models.ForeignKey(Allergies, on_delete=models.CASCADE, blank=True, null=True)
    disabilities = models.ForeignKey(Disabilities, on_delete=models.CASCADE, blank=True, null=True)
    file_documentidentity = models.FileField(upload_to='documents/', blank=True)
    file_v = models.FileField(upload_to='documents/', blank=True)
    file_f = models.FileField(upload_to='documents/', blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_instructors = models.BooleanField()

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Instructors(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    def __str__(self):
        return f"{self.people.name} {self.people.last_name}"


class Sports(models.Model):
    sport_name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    sport_status = models.BooleanField(default=True)

    def __str__(self):
        return self.sport_name


class Athlete(models.Model):
    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    technicalv = models.CharField(max_length=50)
    tacticalv = models.CharField(max_length=50)
    physicalv = models.CharField(max_length=50)
    sports = models.ForeignKey(Sports, on_delete=models.CASCADE)
    athlete_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.people.name} {self.people.last_name}"


class Team(models.Model):
    team_name = models.CharField(max_length=40)
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
    team_image = models.CharField(max_length=255, blank=True, null=True)
    date_create_team = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    description = models.CharField(max_length=250)
    instructors = models.ForeignKey(Instructors, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name


class AthleteTeam(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    dorsal = models.IntegerField()
    positions_initial = models.CharField(max_length=45)
    position_alternative = models.CharField(max_length=45)

    def __str__(self):
        return f"Athlete: {self.athlete.people.name} - Team: {self.team.team_name}"


class Category(models.Model):
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=11)
    category_name = models.CharField(max_length=30)
    date_create_category = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.

    def __str__(self):
        return self.c_name


class Tournaments(models.Model):
    name_tournament = models.CharField(max_length=100)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    max_teams = models.IntegerField()
    max_participants_ethlete = models.IntegerField()
    location = models.CharField(max_length=100)
    prize = models.CharField(max_length=100)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=0)
    enrollment_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name_tournament


class ProgrammingTournaments(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    score = models.IntegerField()
    position = models.IntegerField()
    matches_played = models.IntegerField()
    win = models.IntegerField()
    lose = models.IntegerField()
    tie = models.IntegerField(db_column='Tie')  # Field name made lowercase.
    penalty_score = models.IntegerField()
    registration_date = models.DateField()
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Tournament: {self.tournament.name_tournament} - Date: {self.registration_date}"


class Services(models.Model):
    service_name = models.CharField(max_length=40)
    service_status = models.IntegerField()
    description = models.TextField()
    service_value = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.service_name


class ReceiptPayment(models.Model):
    r_athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    r_service = models.ForeignKey(Services, on_delete=models.CASCADE)
    pay_day = models.DateField()
    full_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Athlete: {self.r_athlete.people.name} - Service: {self.r_service.service_name}"


class Anthropometric(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    controlDate = models.DateField()  # Field name made lowercase.
    arm = models.IntegerField()
    chest = models.CharField(max_length=45)
    hip = models.IntegerField()
    twin = models.IntegerField()
    humerus = models.IntegerField()
    femur = models.IntegerField()
    wrist = models.IntegerField()
    triceps = models.IntegerField()
    supraspinal = models.IntegerField()
    pectoral = models.IntegerField()
    zise = models.IntegerField()
    weight = models.IntegerField()
    bmi = models.IntegerField()
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Athlete: {self.athlete.people.name} - Control Date: {self.controlDate}"


class User(models.Model):
    people = models.ForeignKey(People, models.DO_NOTHING)
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        db_table = 'user'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def get_email_field_name(self):
        return 'people__email'