from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import *
from django.utils.html import format_html
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

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
    groups = models.ManyToManyField(Group, verbose_name='Grupos', blank=True)
    

    def __str__(self):
        return self.name_rol

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        db_table = 'rol'
        ordering = ['name_rol']

class gender(models.Model):
    name_gender = models.CharField(max_length=30, verbose_name="Genero")

    def __str__(self):
        return self.name_gender

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'gender'
        db_table = 'gender'
        ordering = ['id']


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta Email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Utilizar el método set_password para almacenar la contraseña correctamente
        user.is_active = True  # Establecer el usuario como activo
        user.save(using=self._db)

        # Asignar grupos después de crear el usuario
        if 'groups' in extra_fields:
            user.cod_rol.groups.set(extra_fields['groups'])  # Utilizar user.cod_rol en lugar de Rol

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

    # Agregar los campos adicionales de Profile a User
    last_name = models.CharField(max_length=230)
    photo_profile = models.ImageField(upload_to='media/', verbose_name='Imagen del usuario', blank=False)
    birthdate = models.DateField(verbose_name="Fecha de nacimiento")
    gender_user = models.ForeignKey(gender, on_delete=models.CASCADE)
    telephone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener 10 dígitos.')], verbose_name="Teléfono")
    cod_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name='Rol')
    allergies = models.CharField(max_length=250, verbose_name='Alergias')
    disability = models.CharField(max_length=250, verbose_name='Dicapacidad')
    date_create = models.DateField(auto_now_add=True, verbose_name='Fecha de creación')
    type_document = models.ForeignKey(DocumentType, on_delete=models.CASCADE, verbose_name='Tipo de documento')
    num_document = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{8,10}$', "El número de documento debe tener entre 8 y 10 dígitos.")])
    file = models.FileField(upload_to='media/', verbose_name='Documento Consentimiento')
    file_v = models.FileField(upload_to='media/', verbose_name='Documento Visto Medico')
    file_f = models.FileField(upload_to='media/', verbose_name='Documento Fotocopia Del Documento')
    modified_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def clean(self):
    # Validar que el número de documento sea único
        if User.objects.filter(num_document=self.num_document).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un perfil con el mismo número de documento.')
    
    # Validar que el email del usuario sea único
        if User.objects.filter(email=self.email).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un perfil con el mismo correo electrónico.')


    def Imagen_del_usuario(self):
        if self.photo_profile:
            return format_html('<img src="{}" width="100" />', self.photo_profile.url)
        else:
            return ''

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'user'
        ordering = ['date_create']

