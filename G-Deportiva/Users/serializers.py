import django_filters.rest_framework
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = gender
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    photo_profile = serializers.SerializerMethodField()
    password = models.CharField(validators=[RegexValidator(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?!.*\s).*$',
                                 "La contraseña debe contener al menos: 1 letra minúscula, 1 letra mayúscula, 1 número")])
    num_document = models.CharField(validators=[RegexValidator(r'^\d{8,10}$', "El número de documento debe tener entre 8 y 10 dígitos.")])
    phone_number = models.CharField(validators=[RegexValidator(r'^\d{10}$', "El número de teléfono debe tener exactamente 10 dígitos.")])
    email = serializers.EmailField(validators=[])
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False
    )

    photo_profile = serializers.ImageField()

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'name', 'last_name', 'type_document', 'num_document', 'birthdate', 'telephone_number',
            'photo_profile', 'cod_rol', 'gender_user','allergies', 'disability', 'date_create',
            'file', 'file_v', 'file_f', 'modified_at', 'groups', 'is_staff', 'is_active', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password = validated_data.pop('password')
        validated_data['is_active'] = True  # Establecer el usuario como activo
        user = self.Meta.model(**validated_data)  # Utilizar create() para crear la instancia del usuario
        user.set_password(password)  # Establecer la contraseña utilizando set_password()
        user.save()  # Guardar la instancia del usuario

        if groups_data:
            user.cod_rol.groups.set(groups_data)

        return user
    
    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        if groups_data:
            Rol.groups.set(groups_data)
            user.save()

        return user
    
    def get_photo_profile (self, obj):
        return f"http://127.0.0.1:8000{obj.photo_profile.url}"

    




