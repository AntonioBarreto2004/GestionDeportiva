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
def list_special_conditions(request):
    queryset = SpecialConditions.objects.all()
    if queryset.exists():
        serializer = SpecialConditionsSerializer(queryset, many=True)
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados',
            'data': serializer.data
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
def create_special_condition(request):
    """ Para crear una condición especial. """
    data = request.data
    condition_name = data.get('condition_name', None)
    description = data.get('description', None)

    # Validamos que el nombre no esté vacío
    if condition_name is None:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó un nombre para la condición especial',
            'data': None
        })

    # Validamos que la descripción no esté vacía
    if description is None:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una descripción para la condición especial',
            'data': None
        })

    # Validamos que el nombre no esté vacío
    if not condition_name or condition_name.strip() == '':
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó un nombre para la condición especial',
            'data': None
        })

    # Validamos que la descripción no esté vacía
    if not description or description.strip() == '':
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una descripción para la condición especial',
            'data': None
        })

    # Verificamos que el nombre de la condición especial no esté duplicado
    if SpecialConditions.objects.filter(condition_name=condition_name).exists():
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La Condición Especial con ese nombre ya existe',
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

    # Creamos la condición especial una vez superadas todas las validaciones
    condition = SpecialConditions.objects.create(condition_name=condition_name, description=description)
    serializer = SpecialConditionsSerializer(condition)

    return Response({
        'code': status.HTTP_201_CREATED,
        'status': True,
        'message': 'Condición Especial creada con éxito',
        'data': serializer.data
    })

# Resto de funciones (update_special_condition, delete_special_condition) siguen el mismo patrón de la función "update_disability" y "delete_disability", adaptadas para SpecialConditions.

@api_view(['PATCH'])
def update_special_condition(request, condition_id):
    """ Actualiza parcialmente una condición especial """
    try:
        condition = SpecialConditions.objects.get(pk=condition_id)
    except SpecialConditions.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La condición especial no fue encontrada',
        })

    condition_name = request.data.get('condition_name')

    existing_condition = SpecialConditions.objects.filter(condition_name=condition_name).first()
    if existing_condition:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Ya existe una Condición Especial con el mismo nombre.',
                'data': None
            })

    # Validamos que la descripción no supere los 250 caracteres
    description = request.data.get('description', None)
    if description and len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La descripción no debe superar los 250 caracteres',
        })

    serializer = SpecialConditionsSerializer(condition, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Condición especial actualizada exitosamente',
            'data': serializer.data
        })

    return Response({
        'code': status.HTTP_200_OK,
        'status': False,
        'message': 'Error al actualizar la condición especial',
        'data': serializer.errors
    })

@api_view(['DELETE'])
def delete_special_condition(request, condition_id):
    """ Elimina una condición especial """
    try:
        condition = SpecialConditions.objects.get(pk=condition_id)
    except SpecialConditions.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La condición especial no fue encontrada',
        })

    condition.delete()

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Condición especial eliminada exitosamente',
    })
