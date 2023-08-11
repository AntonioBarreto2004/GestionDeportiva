from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_Allergies(request):
    allergie_id = request.GET.get('id')

    if allergie_id:
        try:
            allergie = Allergies.objects.get(pk=allergie_id)
            serializer = AllergiesSerializer(allergie)
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Datos encontrados',
                'data': [serializer.data]
            }
        except Allergies.DoesNotExist:
            response_data = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Alergia no encontrada',
                'data': None
            }
    else:
        queryset = Allergies.objects.all()

        allergie_name = request.GET.get('allergie_name')
        if allergie_name:
            queryset = queryset.filter(allergie_name__icontains=allergie_name)

        if queryset.exists():
            serializer = AllergiesSerializer(queryset, many=True)
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
def create_Allergies(request):
    """ Para crear una alergia. """
    data = request.data
    allergie_name = data.get('allergie_name', None)
    description = data.get('description', None)

    # Validamos que el nombre y la descripción no estén vacíos
    if allergie_name is None or allergie_name.strip() == "":
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'El nombre de la alergia no puede estar vacío',
            'data': None
        })

    if description is None or description.strip() == "":
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La descripción de la alergia no puede estar vacía',
            'data': None
        })

    # Verificamos que el nombre de la alergia no esté duplicado
    if Allergies.objects.filter(allergie_name=allergie_name).exists():
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La alergia con ese nombre ya existe',
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

    # Creamos la alergia una vez superadas todas las validaciones
    allergie = Allergies.objects.create(allergie_name=allergie_name, description=description)
    serializer = AllergiesSerializer(allergie)

    return Response({
        'code': status.HTTP_201_CREATED,
        'status': True,
        'message': 'Alergia creada con éxito',
        'data': serializer.data
    })


@api_view(['PATCH'])
def update_Allergies(request, pk):
    """ Actualiza parcialmente una discapacidad """
    try:
        allergies = Allergies.objects.get(pk=pk)
    except Allergies.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La alergia no fue encontrada',
        })
    
    allergie_name = request.data.get('allergie_name')

    existing_sport = Allergies.objects.filter(allergie_name=allergie_name).first()
    if existing_sport:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Ya existe una Alergia con el mismo nombre.',
                'data': None
            })

    # Validamos que la descripción no supere los 250 caractéres
    description = request.data.get('description', None)
    if description and len(description) > 250:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La descripción no debe superar los 250 caracteres',
        })

    serializer = AllergiesSerializer(allergies, data=request.data, partial=True)
    
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
def delete_Allergies(request, pk):
    """ Elimina una discapacidad """
    try:
        allergies = Allergies.objects.get(pk=pk)
    except Allergies.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La Alergia no fue encontrada',
        })

    allergies.delete()
    
    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Alergia eliminada exitosamente',
    })

