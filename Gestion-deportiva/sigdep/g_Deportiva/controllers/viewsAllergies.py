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
def list_Allergies(request):
    queryset = Allergies.objects.all()
    if queryset.exists():
        serializerDisa = AllergiesSerializer(queryset, many=True)
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados',
            'data': serializerDisa.data
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No hay datos',
            'data': None
        }

    return Response(response_data)


@api_view(['POST'])
def create_Allergies(request):
    """ Para crear una discapacidad. """
    data = request.data
    allergie_name = data.get('allergie_name', None)
    description = data.get('description', None)

    # Validamos que el nombre no esté vacío
    if allergie_name is None:
        return Response({
        'code': status.HTTP_200_OK,
        'status': False,
        'message': 'No se proporcionó un nombre para la Alergia',
        'data': None
        })

    # Validamos que la descripción no esté vacía
    if description is None:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una descripción para la Alergia',
            'data': None
        })

    # Verificamos que el nombre de la discapacidad no esté duplicado
    if Allergies.objects.filter(allergie_name=allergie_name).exists():
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La Aleriga con ese nombre ya existe',
            'data': None
        })

    # Verificamos que la descripción no supere los 250 caracteres
    if len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La descripción no debe superar los 250 caracteres',
            'data': None
        })

    # Creamos la discapacidad una vez superadas todas las validaciones
    disability = Allergies.objects.create(allergie_name=allergie_name, description=description)
    serializer = AllergiesSerializer(disability)

    return Response({
        'code': status.HTTP_201_CREATED,
        'status': True,
        'message': 'Alergia creada con éxito',
        'data': serializer.data
    })


@api_view(['PATCH'])
def update_Allergies(request, allergie_id):
    """ Actualiza parcialmente una discapacidad """
    try:
        disability = Allergies.objects.get(pk=allergie_id)
    except Allergies.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La alergia no fue encontrada',
        })

    # Validamos que la descripción no supere los 250 caractéres
    description = request.data.get('description', None)
    if description and len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La descripción no debe superar los 250 caracteres',
        })

    serializer = AllergiesSerializer(disability, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Alegia actualizada exitosamente',
            'data': serializer.data
        })

    return Response({
        'code': status.HTTP_200_OK,
        'status': False,
        'message': 'Error al actualizar la Alergia',
        'data': serializer.errors
    })

@api_view(['DELETE'])
def delete_Allergies(request, allergie_id):
    """ Elimina una discapacidad """
    try:
        disability = Allergies.objects.get(pk=allergie_id)
    except Allergies.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La Alergia no fue encontrada',
        })

    disability.delete()
    
    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Alergia eliminada exitosamente',
    })

