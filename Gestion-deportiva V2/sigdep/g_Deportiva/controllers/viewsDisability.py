from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_disability(request):
    disability = request.GET.get('id')
    if disability:
        try:
            disability_id = Disabilities.objects.get(pk=disability)
            serializer = DisabilitiesSerializer(disability_id)
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
                'message': 'Datos no encontrada',
                'data': None
            }

    else:   
        queryset = Disabilities.objects.all()

        disability_name = request.GET.get('disability_name')
        if disability_name:
            queryset = queryset.filter(disability_name__icontains=disability_name)
            
        if queryset.exists():
            serializerDisa = DisabilitiesSerializer(queryset, many=True)
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
def create_disability(request):
    """ Para crear una discapacidad. """
    data = request.data
    disability_name = data.get('disability_name', None)
    description = data.get('description', None)

    # Validamos que el nombre no esté vacío
    if disability_name is None:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó un nombre para la discapacidad',
            'data': None
        })

    # Validamos que la descripción no esté vacía
    if description is None:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una descripción para la discapacidad',
            'data': None
        })

    # Validamos que el nombre no esté vacío
    if not disability_name or disability_name.strip() == '':
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó un nombre para la discapacidad',
            'data': None
        })


    # Validamos que la descripción no esté vacía
    if not description or description.strip() == '':
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una descripción para la discapacidad',
            'data': None
        })
    
    # Verificamos que el nombre de la alergia no esté duplicado
    if Disabilities.objects.filter(disability_name=disability_name).exists():
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La Discapacidad con ese nombre ya existe',
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
    disability = Disabilities.objects.create(disability_name=disability_name, description=description)
    serializer = DisabilitiesSerializer(disability)

    return Response({
        'code': status.HTTP_201_CREATED,
        'status': True,
        'message': 'Discapacidad creada con éxito',
        'data': serializer.data
    })


@api_view(['PATCH'])
def update_disability(request, disability_id):
    """ Actualiza parcialmente una discapacidad """
    try:
        disability = Disabilities.objects.get(pk=disability_id)
    except Disabilities.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La discapacidad no fue encontrada',
        })
    
    disability_name = request.data.get('disability_name')

    existing_sport = Disabilities.objects.filter(disability_name=disability_name).first()
    if existing_sport:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Ya existe una Discapacidad con el mismo nombre.',
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

    serializer = DisabilitiesSerializer(disability, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

        return Response({
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Discapacidad actualizada exitosamente',
            'data': serializer.data
        })

    return Response({
        'code': status.HTTP_200_OK,
        'status': False,
        'message': 'Error al actualizar la discapacidad',
        'data': serializer.errors
    })

@api_view(['DELETE'])
def delete_disability(request, disability_id):
    """ Elimina una discapacidad """
    try:
        disability = Disabilities.objects.get(pk=disability_id)
    except Disabilities.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La discapacidad no fue encontrada',
        })

    disability.delete()
    
    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Discapacidad eliminada exitosamente',
    })

