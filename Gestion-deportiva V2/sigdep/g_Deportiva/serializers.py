from rest_framework import serializers
from .models import *



class DisabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities
        fields = ['id', 'disability_name', 'description']

class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ('id', 'allergie_name', 'description')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id','name_rol', 'description')

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
    user = UserSerializer(required=False)  # Cambiamos a required=False para que sea opcional
    rol_name = serializers.CharField(source='users.rol.name', read_only=True)

    def to_internal_value(self, data):
        allergies_value = data.get('allergies', None)
        disabilities_value = data.get('disabilities', None)

        # Transformar "0" a None (null) si es necesario
        if allergies_value == 0:
            data['allergies'] = None
        if disabilities_value == 0:
            data['disabilities'] = None

        return super().to_internal_value(data)

    class Meta:
        model = People
        fields = ['id','user', 'name', 'last_name', 'email', 'photo_user', 'birthdate', 'gender', 'telephone_number',
                  'type_document_id', 'num_document', 'allergies', 'disabilities', 'file_documentidentity',
                  'file_v', 'file_f', 'modified_at', 'rol_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)  # Si no se proporciona 'user', establecer como None
        people = People.objects.create(**validated_data)

        if user_data:
            user = User.objects.create_user(username=people.email, password=user_data['password'])
            user.rol_id = user_data['rol']
            user.people = people  # Asignar la relación a través de la clave foránea
            user.save()

        return people
    

class SportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sports
        fields = ('id','sport_name', 'description', 'created_at', 'sport_status')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('instructors', 'sport','team_name',  'team_image', 'description', 'date_create_team')

class InstructorSerializer(serializers.ModelSerializer):
    people = serializers.StringRelatedField()

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
        fields = ('id', 'sport', 'category_type', 'category_name', 'date_create_category')

    
class AthleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Athlete
        fields = ('id', 'instructor', 'people', 'sports', 'technicalv', 'tacticalv', 'physicalv', 'athlete_status')