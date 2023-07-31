import re
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django_filters import rest_framework as filters

from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_users(request):
    try:
        # Obtener los parámetros de consulta
        email = request.query_params.get('email')
        name = request.query_params.get('name')
        last_name = request.query_params.get('last_name')
        birthdate = request.query_params.get('birthdate')
        gender = request.query_params.get('gender')
        date_create = request.query_params.get('date_create')
        type_document_id = request.query_params.get('type_document_id')
        num_document = request.query_params.get('num_document')
        rol = request.query_params.get('rol')

        # Crear un diccionario con los parámetros de consulta que se proporcionaron
        filters = {}
        if email:
            filters['email__icontains'] = email
        if name:
            filters['name__icontains'] = name
        if last_name:
            filters['last_name__icontains'] = last_name
        if birthdate:
            filters['birthdate'] = birthdate
        if gender:
            filters['gender__icontains'] = gender
        if date_create:
            filters['date_create'] = date_create
        if type_document_id:
            filters['type_document_id__icontains'] = type_document_id
        if num_document:
            filters['num_document'] = num_document
        if rol:
            filters['rol__name__icontains'] = rol

        # Obtener todos los objetos People y User que coincidan con los parámetros de consulta
        people = People.objects.filter(**filters)
        users = User.objects.filter(people__in=people)

        # Comprobar si hay datos
        if not people and not users:
            return Response(
                data={
                    'code': status.HTTP_204_NO_CONTENT, 
                    'status': False, 
                    'message': 'No hay datos disponibles',
                    'data': None
                }
            )

        # Serializar los objetos
        people_serializer = PeopleSerializer(people, many=True)
        user_serializer = UserSerializer(users, many=True)

        # Devolver la respuesta
        return Response(
            data={
                'code': status.HTTP_200_OK, 
                'status': True, 
                'message': 'Listado de usuarios y personas obtenido exitosamente',
                'data': {
                    'people': people_serializer.data,
                    'users': user_serializer.data
                }
            }
        )

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)



# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/correo.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)


@api_view(['POST'])
def create_user(request):
    try:
        data = request.data

        # Extraer los campos
        email = data.get('email')
        name = data.get('name')
        last_name = data.get('last_name')
        num_document = data.get('num_document')
        user_data = data.get('user')

        # Aquí es donde realizamos las validaciones
        empty_fields = []
        if not email:
            empty_fields.append('Correo')
        if not name:
            empty_fields.append('Nombre')
        if not last_name:
            empty_fields.append('apellido')
        if not num_document:
            empty_fields.append('Numero de documento')
        if not user_data:
            empty_fields.append('Uusario')
        else:
            rol = user_data.get('rol')
            password = user_data.get('Contraseña')
            if not rol:
                empty_fields.append('rol')
            if not password:
                empty_fields.append('Contraseña')

        if empty_fields:
            return Response(
                data={'code': status.HTTP_200_OK, 
                      'message': 'Los campos no pueden estar vacíos',
                      'status': False, 
                      'data': empty_fields
                     },
                status=status.HTTP_200_OK
            )

        # Realizar verificación adicional para evitar usuarios duplicados
        if People.objects.filter(email=email).exists():
            return Response(
                data={'code': status.HTTP_200_OK, 
                    'message': 'Ya existe un usuario con este correo registrado', 
                    'status': False, 
                    'data': None
                    },
                status=status.HTTP_200_OK
            )

        if People.objects.filter(num_document=num_document).exists():
            return Response(
                data={'code': status.HTTP_200_OK, 
                    'message': 'Ya existe un usuario con este número de documento', 
                    'status': False, 
                    'data': None
                    },
                status=status.HTTP_200_OK
            )

        # Validaciones para el nombre y apellido
        if not name or not last_name:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El nombre y apellido del usuario no pueden estar vacíos.',
                'status': False
            }
            return Response(response_data)

        elif not re.match(r'^[a-zA-Z\s]+$', name) or not re.match(r'^[a-zA-Z\s]+$', last_name):
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El nombre y apellido del usuario solo pueden contener letras y espacios.',
                'status': False
            }
            return Response(response_data)

        # Validación para el num_document
        if not re.fullmatch(r'^\d{8,10}$', str(num_document)):
            response_data = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El número de documento debe tener entre 8 y 10 dígitos.',
                'data': None
            }
            return Response(response_data)

        # Validación para el password
        if not re.fullmatch(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.{12,}).*$', password):
            response_data = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'La contraseña debe tener más de 12 caracteres, contener al menos una letra mayúscula, una letra minúscula y un número.',
                'data': None
            }
            return Response(response_data)

        user_serializer = UserSerializer(data=data.get('user'))
        people_serializer = PeopleSerializer(data=data)

    # Aquí es donde creamos y guardamos el objeto People primero
        if people_serializer.is_valid():
            people = people_serializer.save()

            # Ahora que tenemos un objeto People, podemos usar su ID para crear el objeto User
            user_data = data.get('user')
            user_data['people'] = people.id
            user_serializer = UserSerializer(data=user_data)

            if user_serializer.is_valid():
                user = user_serializer.save()
            # Enviar correo de activación
            send_activation_email(name, email, password)

            response_data = {
                'code': status.HTTP_201_CREATED,
                'status': True,
                'message': 'Usuario creado exitosamente',
                'data': None
            }
            return Response(response_data)
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)