from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class Allergies(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'allergies'


class Disabilities(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'disabilities'
    
class specialconditions(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'specialconditions'
    
class Rol(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'rol'


class People(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=230)
    photo_user = models.ImageField(upload_to='media/', blank=True, null=True)  # Permite que el campo sea opcional
    birthdate = models.DateField()
    gender = models.CharField(max_length=9)
    telephone_number = models.CharField(max_length=10)
    date_create = models.DateField(auto_now_add=True)
    type_document = models.CharField(max_length=20)
    num_document = models.IntegerField()
    file_documentidentity = models.FileField(upload_to='documents/', blank=True)
    file_eps_certificate = models.FileField(upload_to='documents/', blank=True)
    file_informed_consent = models.FileField(upload_to='documents/', blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    class Meta:
        db_table = 'people'

    
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
    

class Instructors(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    def __str__(self):
        return f"{self.people.name} {self.people.last_name}"
    
    class Meta:
        db_table = 'instructors'
    
    
class peopleallergies(models.Model):
    people = models.ForeignKey(People, models.DO_NOTHING)
    allergies = models.ForeignKey(Allergies, on_delete=models.CASCADE)

    class Meta:
        db_table = 'peopleallergies'


class peopleDisabilities(models.Model):
    people = models.ForeignKey(People, models.DO_NOTHING)
    disabilities = models.ForeignKey(Disabilities, on_delete=models.CASCADE)

    class Meta:
        db_table = 'peopledisabilities'

class peoplespecialConditions(models.Model):
    people = models.ForeignKey(People, models.DO_NOTHING)
    specialconditions = models.ForeignKey(specialconditions, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'peoplespecialconditions'

    
class Sports(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'sports'

class Athlete(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    technical = models.CharField(max_length=50)
    tactical = models.CharField(max_length=50)
    physical = models.CharField(max_length=50)
    sports = models.ForeignKey(Sports, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.people.name} {self.people.last_name}"
    
    class Meta:
        db_table = 'athlete'

class AthleteInstructor(models.Model):
    athlete =  models.ForeignKey(Athlete, on_delete=models.CASCADE)
    instructor =  models.ForeignKey(Instructors, on_delete=models.CASCADE)

    class Meta:
        db_table = 'athlete_instructor'

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'specialization'

class Instructor_specialization(models.Model):
    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'instructor_specialization'


class Team(models.Model):
    name = models.CharField(max_length=40)
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, blank=True, null=True)
    date_create_team = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    description = models.CharField(max_length=250)
    instructors = models.ForeignKey(Instructors, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'team'


class AthleteTeam(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    dorsal = models.IntegerField()
    positions_initial = models.CharField(max_length=45)
    position_alternative = models.CharField(max_length=45)

    def __str__(self):
        return f"Athlete: {self.athlete.people.name} - Team: {self.team.team_name}"

    class Meta:
        db_table = 'athleteTeam'

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=250)
    date_create_category = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'

    
class CategorySport(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    sport_id  = models.ForeignKey(Sports, on_delete=models.CASCADE)

    class Meta:
        db_table = 'categorySport'

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
    
    class Meta:
        db_table = 'tournaments'


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

    class Meta:
        db_table = 'programmingTournaments'

class Services(models.Model):
    name = models.CharField(max_length=40)
    status = models.IntegerField()
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'services'


class ReceiptPayment(models.Model):
    r_athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    r_service = models.ForeignKey(Services, on_delete=models.CASCADE)
    pay_day = models.DateField()
    full_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Athlete: {self.r_athlete.people.name} - Service: {self.r_service.service_name}"

    class Meta:
        db_table = 'receiptPayment'

class Anthropometric(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    controlDate = models.DateField(auto_now_add=True)  # Field name made lowercase.
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

    class Meta:
        db_table = 'anthropometric'
