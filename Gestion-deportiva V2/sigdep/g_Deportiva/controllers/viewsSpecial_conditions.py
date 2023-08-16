from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_special_conditions(request):
    special_conditions = request.GET.get('id')
    if special_conditions:
        try:
            special_conditions_id = specialconditions.objects.get(pk=special_conditions)
            serializer = specialConditionsSerializer(special_conditions_id)
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Datos encontrados',
                'data': [serializer.data]
            }
        except specialconditions.DoesNotExist:
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Datos no encontrada',
                'data': None
            }
    else:
        queryset = specialconditions.objects.all()

        specialConditions_name = request.GET.get('name')
        if specialConditions_name:
            queryset = queryset.filter(name__icontains=specialConditions_name)
            
        if queryset.exists():
            serializer = specialConditionsSerializer(queryset, many=True)
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Datos encontrados',
                'data': serializer.data
            }
        else:
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'No hay datos',
                'data': None
            }

        return Response(response_data)
    

@api_view(['POST'])
def create_special_condition(request):
    """ Para crear una condición especial. """
    data = request.data
    condition_name = data.get('specialConditions_name', None)
    description = data.get('description', None)

    # Validamos que el nombre no esté vacío
    if condition_name is None or not condition_name.strip():
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se proporcionó un nombre para la condición especial',
            'data': None
        })

    # Validamos que la descripción no esté vacía
    if description is None or not description.strip():
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se proporcionó una descripción para la condición especial',
            'data': None
        })

    # Verificamos que el nombre de la condición especial no esté duplicado
    if specialconditions.objects.filter(specialConditions_name=condition_name).exists():
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'La Condición Especial con ese nombre ya existe',
            'data': None
        })

    # Verificamos que la descripción no supere los 250 caracteres
    if len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'La descripción no debe superar los 250 caracteres',
            'data': None
        })

    # Creamos la condición especial una vez superadas todas las validaciones
    condition = specialconditions.objects.create(specialConditions_name=condition_name, description=description)
    serializer = specialConditionsSerializer(condition)

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Condición Especial creada con éxito',
        'data': serializer.data
    })

@api_view(['PUT'])
def update_special_condition(request, condition_id):
    """ Actualiza una condición especial de manera parcial o completa """
    try:
        condition = specialconditions.objects.get(pk=condition_id)
    except specialconditions.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'La condición especial no fue encontrada',
        })

    condition_name = request.data.get('specialConditions_name')

    if condition_name:
        existing_condition = specialconditions.objects.filter(specialConditions_name=condition_name).exclude(pk=condition_id).first()
        if existing_condition:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'Ya existe una Condición Especial con el mismo nombre.',
                    'data': None
                })

    # Validamos que la descripción no supere los 250 caracteres
    description = request.data.get('description', None)
    if description and len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'La descripción no debe superar los 250 caracteres',
        })

    serializer = specialConditionsSerializer(condition, data=request.data, partial=True)

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
        'status': True,
        'message': 'Error al actualizar la condición especial',
        'data': serializer.errors
    })

@api_view(['DELETE'])
def delete_special_condition(request, pk):
    """ Elimina una condición especial """
    try:
        condition = specialconditions.objects.get(pk=pk)
        condition.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Condición especial eliminada exitosamente',
        })
    except specialconditions.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'La condición especial no fue encontrada',
        })