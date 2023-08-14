import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_category(request):
    queryset = Category.objects.all()
    serializer = CategorySerializer(queryset, many=True)
    
    if queryset.exists():
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
def create_category(request):
    data = request.data

    # Obtener los datos de la categoría del JSON enviado en la solicitud
    category_type = data.get('category_type')
    category_name = data.get('category_name')
    description = data.get('description')

    # Verificar si los campos requeridos están vacíos
    empty_fields = []
    required_fields = ['category_type', 'category_name', 'description']
    for field in required_fields:
        if not data.get(field):
            empty_fields.append(field)

    if empty_fields:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Los siguientes campos no pueden estar vacíos: ',
            'status': ' + '.join(empty_fields)
        }
        return Response(response_data)

    # Verificar si el tipo de categoría solo contiene letras y espacios
    if not re.match(r'^[a-zA-Z\s]+$', category_type):
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'El Tipo de Categoria solo pueden contener letras y espacios.',
            'status': False
        }
        return Response(response_data)

    # Verificar si ya existe una categoría con el mismo nombre
    if Category.objects.filter(category_name=category_name).exists():
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Ya existe una categoría con el mismo nombre.',
            'data': None
        }
        return Response(response_data)

    # Crear una instancia de Category utilizando los datos proporcionados
    category_data = {
        'category_type': category_type,
        'category_name': category_name,
        'description': description
    }

    category_create = CategorySerializer(data=category_data)
    if category_create.is_valid():
        category_create.save()
        response_data = {
            'code': status.HTTP_201_CREATED,
            'status': True,
            'message': f'Categoría {category_name} creada exitosamente',
            'data': {
                'category_name': category_name,
                'description': description
            }
        }
        return Response(response_data)

# Resto de las vistas (update_category, delete_category) se mantienen igual


@api_view(['PATCH'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'Categoría no encontrada',
            'data': None
        }
        return Response(response_data)
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Categoría actualizada exitosamente',
            'data': serializer.data
        }
    else:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Error al actualizar la categoría',
            'data': serializer.errors
        }
    return Response(response_data)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Categoría no encontrada',
            'data': None
        }
        return Response(response_data)
    
    category_name = category.category_name
    category.delete()

    response_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': f'Categoría {category_name} eliminada exitosamente',
        'data': None
    }
    
    return Response(response_data)
