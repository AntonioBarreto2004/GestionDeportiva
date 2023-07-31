from rest_framework import serializers
from .models import *



class DisabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities
        fields = ['id', 'disability_name', 'description']

class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ['id', 'allergie_name', 'description']


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['rol','is_active', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['is_active'] = True  # Establecer el usuario como activo
        user = self.Meta.model(**validated_data)  # Utilizar create() para crear la instancia del usuario
        user.set_password(password)  # Establecer la contraseña utilizando set_password()
        user.save()  # Guardar la instancia del usuario

        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class PeopleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photo_user = serializers.ImageField(required=False)

    class Meta:
        model = People
        fields = ['user', 'name', 'last_name', 'email', 'photo_user', 'birthdate', 'gender', 'telephone_number',
                  'type_document_id', 'num_document', 'allergies', 'disabilities', 'file',
                  'file_v', 'file_f', 'modified_at', 'is_instructors']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        people, created = People.objects.update_or_create(user=user, **validated_data)
        return people
    

class SportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sports
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'