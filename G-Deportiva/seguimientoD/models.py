from django.db import models
from django.conf import settings
from Users.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    t_name = models.CharField(max_length=30, verbose_name='Deporte')
    c_name = models.CharField(max_length=30, verbose_name='Tipo de Categoría')
    date_create_Category = models.DateField(auto_now_add=True, name='Fecha de Creacion')
    def __str__(self):
        return self.t_name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        db_table = 'category'

class Positions(models.Model):
    p_category = models.ForeignKey(Category, verbose_name="Deporte", on_delete=models.CASCADE)
    at_position = models.CharField(max_length=50, verbose_name='Posición Principal')
    at_positiona = models.CharField(max_length=50, verbose_name='Posición Alternativa')

    def __str__(self):
        return self.at_position

    class Meta:
        verbose_name = 'Posición'
        verbose_name_plural = 'Posiciones'
        db_table = 'positions'


class Team(models.Model):
    team_name = models.CharField(max_length=40, verbose_name='Nombre de equipo')
    team_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    team_image = models.ImageField(upload_to='media/', blank=False, verbose_name='Foto del Equipo')
    team_user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Instructor')
    date_create_Team = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __str__(self):
        return self.team_name

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        db_table = 'team'


class Athlete(models.Model):
    at_user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Atleta')
    dorsal = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99)
        ],
        verbose_name='Dorsal Jugador'
    )
    a_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Deporte')
    at_team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Equipo')
    c_position = models.ForeignKey(Positions, on_delete=models.CASCADE, related_name='posicion_inicial', verbose_name='Posición Principal')
    c_positiona = models.ForeignKey(Positions, on_delete=models.CASCADE, related_name='posicion_alterna', verbose_name='Posición Alterna')
    at_technicalv = models.CharField(max_length=50, verbose_name='Valoración Técnica')
    at_tacticalv = models.CharField(max_length=50, verbose_name='Valoración Táctica')
    at_physicalv = models.CharField(max_length=50, verbose_name='Valoración Física')

    def __str__(self):
        return str(self.at_user)

    class Meta:
       verbose_name = 'Atleta'
       verbose_name_plural = 'Atletas'
       db_table = 'athlete' 


class Anthropometric(models.Model):
    athlete_id = models.ForeignKey(Athlete, on_delete=models.CASCADE, verbose_name='Atleta')
    atpt_controlDate = models.DateField(verbose_name='Fecha de Control')
    atpt_arm = models.IntegerField(verbose_name='Brazo')
    atpt_chest = models.CharField(max_length=45, verbose_name='Pecho')
    atpt_hip = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Cadera')
    atpt_calf = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Gemelo')
    atpt_humerus = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Húmero')
    atpt_femur = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Fémur')
    atpt_wrist = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Muñeca')
    atpt_triceps = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Tríceps')
    atpt_suprailiac = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Supraespinal')
    atpt_pectoral = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Pectoral')
    atpt_height = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Talla')
    atpt_weight = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Peso')
    atpt_bmi = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='IMC')
    atpt_created_date = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    atpt_updated_date = models.DateField(auto_now=True, verbose_name='Fecha Actualización')

    def __str__(self):
        return str(self.athlete_id)

    class Meta:
        verbose_name = 'Antropométrica'
        verbose_name_plural = 'Antropométricas'
        db_table = 'anthropometric' 
        
class Sports(models.Model):
    id=models.IntegerField
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name








