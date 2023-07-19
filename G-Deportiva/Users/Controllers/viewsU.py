from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status

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
            data={'code': '404_NOT_FOUND', 'message': 'Usuario no existe', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UserSerializer(filtered_queryset, many=True)
    return Response(serializer.data)

#Registrar
# Usuarios y envio de Correo.
# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/email.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)


@api_view(['POST'])
def create_user(request):
    serializerU = UserSerializer(data=request.data)
    serializerU.is_valid(raise_exception=True)
    validated_data = serializerU.validated_data

    num_document = validated_data['num_document']

    # Realizar verificación adicional para evitar usuarios duplicados
    if get_user_model().objects.filter(email=validated_data['email']).exists():
        return Response(
            data={'code': '409_CONFLICT', 'message': 'Ya existe un usuario con este correo registrado', 'status': False}, 
            status=status.HTTP_409_CONFLICT
        )
     # Realizar verificación adicional para evitar usuarios duplicados
    if get_user_model().objects.filter(num_document=num_document).exists():
        return Response(
            data={'code': '409_CONFLICT', 'message': 'Ya existe un usuario con este número de documento', 'status': False},
            status=status.HTTP_409_CONFLICT
        )
    
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
        'code': '201_CREATED',
        'message': 'Usuario creado exitosamente, se le ha enviado un correo',
        'status': True,
        'photo_profile': user.photo_profile.url  # Agregar la URL de la foto de perfil asignada
    }

    return Response(data=response_data, status=status.HTTP_201_CREATED)



#Editar Usuario determinado.
@api_view(['PATCH'])
def update_user(request, pk):
    try:
        userU = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no existe',  'status':False}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    serializerUd = UserSerializer(userU, data=request.data, partial=True)
    serializerUd.is_valid(raise_exception=True)
    serializerUd.save()
    
    return Response(
        data={'code':'202_ACCEPTED', 'message': 'Usuario Actualizado exitosamente',  'status':True}, 
        status=status.HTTP_202_ACCEPTED
    )

#Eliminar Usuario determinado.
@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no existe',  'status':False}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    user.delete()
    return Response(
        data={'code':'204_NO_CONTENT', 'message': 'Usuario eliminado exitosamente',  'status':True}, 
        status=status.HTTP_204_NO_CONTENT
    )


