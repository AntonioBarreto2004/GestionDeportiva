import base64
from rest_framework import serializers
from django.utils import baseconv
from .models import *


class DisabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities
        fields = ['id', 'name', 'description','status']

class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ('id', 'name', 'description','status')

class specialConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = specialconditions
        fields = ('id', 'name', 'description','status')

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id','name', 'description','status')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['rol', 'is_active', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'is_active': {'default': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class PeopleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    rol_name = serializers.CharField(source='users.rol.name', read_only=True)
    photo_user = serializers.ImageField(required=False, read_only=True)
    file_documentidentity = serializers.FileField(required=False, read_only=True)
    file_eps_certificate = serializers.FileField(required=False, read_only=True)
    file_informed_consent = serializers.FileField(required=False, read_only=True)

    def to_internal_value(self, data):
        allergies_value = data.get('allergies', None)
        disabilities_value = data.get('disabilities', None)

        if allergies_value == 0:
            data['allergies'] = None
        if disabilities_value == 0:
            data['disabilities'] = None

        return super().to_internal_value(data)

    class Meta:
        model = People
        fields = ['id', 'user', 'name', 'last_name', 'email', 'photo_user', 'birthdate', 'gender', 'telephone_number',
                  'type_document', 'num_document', 'file_documentidentity',
                  'file_eps_certificate', 'file_informed_consent', 'modified_at', 'rol_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)  # Si no se proporciona 'user', establecer como None
        people = People.objects.create(**validated_data)

        if user_data:
            user = User.objects.create_user(username=people.email, password=user_data['password'])
            user.rol_id = user_data['rol']
            user.people = people  # Asignar la relación a través de la clave foránea
            user.save()

        return people
    
    def update(self, instance, validated_data):
        # Manejar campos de archivo por separado antes de actualizar
        photo_user = validated_data.pop('photo_user', None)
        file_documentidentity = validated_data.pop('file_documentidentity', None)
        file_eps_certificate = validated_data.pop('file_eps_certificate', None)
        file_informed_consent = validated_data.pop('file_informed_consent', None)

        # Actualizar otros campos
        instance = super().update(instance, validated_data)

        # Actualizar campos de archivo si se proporcionaron en la solicitud
        if photo_user:
            instance.photo_user = photo_user
        if file_documentidentity:
            instance.file_documentidentity = file_documentidentity
        if file_eps_certificate:
            instance.file_eps_certificate = file_eps_certificate
        if file_informed_consent:
            instance.file_informed_consent = file_informed_consent

        instance.save()  # Guardar cambios en campos de archivo

        return instance
    
    

class SportsSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        required=False  # La lista de IDs de categorías es opcional
    )
    class Meta:
        model = Sports
        fields = ('id','name', 'description', 'created_at', 'status', 'category_ids')

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])  # Remove category_ids from validated_data
        sport = Sports.objects.create(**validated_data)

        for category_id_data in category_ids:
            category_id = category_id_data.get('id')
            try:
                category = Category.objects.get(pk=category_id)
                CategorySport.objects.get_or_create(category_id=category, sport_id=sport)
            except Category.DoesNotExist:
                pass

        return sport

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('instructors', 'sport', 'name',  'image', 'description', 'date_create_team')

class InstructorSerializer(serializers.ModelSerializer):
    people = PeopleSerializer() 
    class Meta:
        model = Instructors
        fields = ['id', 'people', 'specialization', 'experience_years']


class AnthropometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anthropometric
        fields = ('id', 'athlete', 'controlDate', 'arm', 'chest', 'hip', 'twin', 'humerus', 'femur',
                  'wrist', 'triceps', 'supraspinal', 'pectoral', 'zise', 'weight', 'bmi', 'updated_date')
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name','description', 'date_create_category')

    
class AthleteSerializer(serializers.ModelSerializer):
    sports = SportsSerializer(required=False)
    
    class Meta:
        model = Athlete
        fields = ('id', 'people', 'sports', 'technical', 'tactical', 'physical', 'status')

