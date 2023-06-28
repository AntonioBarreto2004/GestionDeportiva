from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django import forms
from django.utils.html import format_html
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta Email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class DocumentType(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'
        db_table = 'document_type'
        ordering = ['name']


class Rol(models.Model):
    name_rol = models.CharField(max_length = 20, verbose_name="Nombre rol")
    

    def __str__(self):
        return self.name_rol

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        db_table = 'rol'
        ordering = ['name_rol']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    photo_profile = models.ImageField(upload_to= 'media', verbose_name='Imagen del usuario', blank=False)
    birthdate = models.DateField(verbose_name="Fecha de nacimiento")
    gender_CHOISE = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('P', 'Prefiero no decir'),
    )
    gender = models.CharField(max_length=9, choices=gender_CHOISE, default='', verbose_name="Genero") 
    telephone_number = models.IntegerField(validators=[
            MinValueValidator(1000000000, message='El número debe tener 10 dígitos'),
            MaxValueValidator(9999999999, message='El número debe tener 10 dígitos')
        ],verbose_name="Telefono")
    cod_rol = models.ForeignKey(Rol, on_delete=models.CASCADE , verbose_name='Rol')
    allergies =models.CharField(max_length=250, verbose_name='Alergias', blank=True)
    disability = models.CharField(max_length=250, verbose_name='Dicapacidad', blank=True)
    state = models.BooleanField(verbose_name = "Estado del usuario", default = True)
    date_create = models.DateField(auto_now_add=True, verbose_name='Fecha de creación')
    type_document = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name='Tipo de documento')
    num_document = models.IntegerField(validators=[MaxValueValidator(9999999999)], verbose_name='Número de documento')
    file = models.FileField(upload_to='media/', verbose_name='Documento Consentimiento')
    file_v = models.FileField(upload_to='media/', verbose_name='Documento Visto Medico')
    file_f = models.FileField(upload_to='media/', verbose_name='Documento Fotocopia Del Documento')

    def Imagen_del_usuario(self):
        return format_html('<img src={} width="100" /> ', self.photo_profile.url)

    def __str__(self):
        return self.user.get_full_name()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'user'
        ordering = ['date_create']

