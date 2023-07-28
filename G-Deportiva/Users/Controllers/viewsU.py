import re
import requests
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from g_deprotiva import settings
from django_filters import rest_framework as filters
from ..models import *
from ..serializers import *

 #Listar Usuarios
@api_view(['GET'])
def list_users(request):
    class UserFilter(filters.FilterSet):
        class Meta:
            model = User
            fields = {
            'id': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'birthdate': ['exact', 'year__gt', 'year__lt'],
            'telephone_number': ['exact'],
            'cod_rol': ['exact'],
            'date_create': ['exact', 'year__gt', 'year__lt'],
            'type_document': ['exact'],
            'num_document': ['exact'],
        }

    queryset = User.objects.all()
    user_filter = UserFilter(request.query_params, queryset=queryset)
    filtered_queryset = user_filter.qs

    if not filtered_queryset.exists():
        return Response(
            data={'code': status.HTTP_200_OK, 'message': 'Usuario no existe', 'status': False,'data': None},
        )

    serializer = UserSerializer(filtered_queryset, many=True)
    return Response(serializer.data)

#Registrar
# Usuarios y envio de Correo.
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
        serializerU = UserSerializer(data=request.data)
        if serializerU.is_valid(raise_exception=True):
            validated_data = serializerU.validated_data

            name = serializerU.validated_data['name']
            last_name = serializerU.validated_data['last_name']
            num_document = validated_data['num_document']
            num_document = validated_data.get('num_document')
            password = validated_data.get('password')

            # Realizar verificación adicional para evitar usuarios duplicados
            if get_user_model().objects.filter(email=validated_data['email']).exists():
                return Response(
                    data={'code': status.HTTP_200_OK, 
                        'message': 'Ya existe un usuario con este correo registrado', 
                        'status': False, 
                        'data': None
                        }, 
                )
            # Realizar verificación adicional para evitar usuarios duplicados
            if get_user_model().objects.filter(num_document=num_document).exists():
                return Response(
                    data={'code': status.HTTP_200_OK, 
                        'message': 'Ya existe un usuario con este número de documento', 
                        'status': False, 
                        'data': None},
                )
            
            if not name and last_name:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del usuario no puede estar vacío.',
                    'status': False
                }
                return Response(response_data)
            
            elif not re.match(r'^[a-zA-Z\s]+$', name and last_name):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del usuario solo puede contener letras y espacios.',
                    'status': False
                }
                return Response(response_data)
            
            if not last_name:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del usuario no puede estar vacío.',
                    'status': False
                }
                return Response(response_data)
            
            elif not re.match(r'^[a-zA-Z\s]+$', last_name):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del usuario solo puede contener letras y espacios.',
                    'status': False
                }
                return Response(response_data)

            # Validación para el num_document
            if not re.fullmatch(r'^\d{8,10}$', num_document):
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
            

        photo_profile = request.FILES.get('photo_profile')
        if photo_profile:
            serializerU.validated_data['photo_profile'] = photo_profile
            
            user_name = validated_data['name']
            user_email = validated_data['email']
            user_password = validated_data['password']
            send_activation_email(user_name, user_email, user_password)
            serializerU.save()

            #ASIGNAR FOTO DE PERFIL AUTOMATICAMENTE
            user = serializerU.instance
            user.photo_profile = request.data['photo_profile']
            user.save()
            # Verificar la asignación de la foto de perfil
            print(f'Foto de perfil asignada: {user.photo_profile}')  # Imprimir la foto de perfil asignada

            # Construir la respuesta incluyendo la foto de perfil
            response_data = {
                'code':  status.HTTP_201_CREATED,
                'message': 'Usuario creado exitosamente, se le ha enviado un correo',
                'status': True,
                'data':None,
                'photo_profile': user.photo_profile.url  # Agregar la URL de la foto de perfil asignada
            }

            return Response(response_data)
        
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Datos invalidos',
            'status': False,
            'errors': serializerU.errors
        }
        return Response(response_data)

    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)



@api_view(['PATCH'])
def update_user(request, pk):
    try:
        userU = User.objects.get(pk=pk)
        serializer = UserSerializer(User, data=request.data, partial=True)

        if 'photo_profile' in request.FILES:
            userU.photo_profile = request.FILES['photo_profile']

    except User.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK, 
                  'message': 'Usuario no existe',  
                  'status': False,
                  'data': None
                  }, 
        )

    name = request.data.get('name')  # Obtén el nombre de los datos de la solicitud
    last_name = request.data.get('last_name')  # Obtén el apellido de los datos de la solicitud

    if name and not re.match(r'^[a-zA-Z\s]+$', name):
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Nombre del usuario solo puede contener letras y espacios.',
            'status': False
        }
        return Response(response_data)

    if last_name and not re.match(r'^[a-zA-Z\s]+$', last_name):
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Apellido del usuario solo puede contener letras y espacios.',
            'status': False
        }
        return Response(response_data)
    
    # Nuevas validaciones
    non_updateable_fields = ['birthdate', 'num_document']
    for field in non_updateable_fields:
        if field in request.data:
            return Response(
                data={'code': status.HTTP_400_BAD_REQUEST, 
                      'message': f'No se puede actualizar el campo: {field}',  
                      'status': False,
                      'data': None
                      }, 
            )
    num_telefono = request.data.get('num_telefono')
    if num_telefono and not re.fullmatch(r'^\d{10}$', num_telefono):
        return Response(
            data={'code': status.HTTP_400_BAD_REQUEST, 
                  'message': 'El número de teléfono debe tener exactamente 10 dígitos.',  
                  'status': False,
                  'data': None
                  }, 
        )
    # Continúa con la operación normal de actualización
    serializerUd = UserSerializer(userU, data=request.data, partial=True)
    serializerUd.is_valid(raise_exception=True)
    # Actualizar el campo modified_at con la fecha y hora actual
    modification_data = userU.modified_at = timezone.now()

    serializer.is_valid(raise_exception=True)
    serializerUd.save()
    
    return Response (
        data={'code': status.HTTP_202_ACCEPTED, 
              'message': 'Usuario Actualizado exitosamente',  
              'status': True,  
              'data': modification_data}, 
    )


#Eliminar Usuario determinado.
@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK, 'message': 'Usuario no existe',  'status':False, 'data': None},         )
    
    user.delete()
    return Response(
        data={'code': status.HTTP_204_NO_CONTENT, 'message': 'Usuario eliminado exitosamente',  'status':True , 'data': None}, 
    )


