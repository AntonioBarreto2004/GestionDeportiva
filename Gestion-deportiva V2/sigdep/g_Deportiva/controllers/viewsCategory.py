from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import re

@api_view(['GET'])
def list_category(request):
    category_name = request.GET.get('category_name')
    category_id = request.GET.get('category_id')  

    # Filtrar las categorías si se proporcionan los parámetros de filtro
    list_category = Category.objects.all()

    if category_name:
        list_category = list_category.filter(category_name=category_name)
    if category_id:  
        list_category = list_category.filter(id=category_id)

    if not list_category:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No hay datos registrados',
            'data': None
        }
        return Response(response_data)

    data = []

    for item in list_category:
        serializer_ctg = CategorySerializer(item)
        item_data = serializer_ctg.data
        data.append(item_data)

    response_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos encontrados',
        'data': data
    }
    return Response(response_data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import re

@api_view(['GET'])
def list_category(request):
    category_name = request.GET.get('category_name')
    category_id = request.GET.get('category_id')  

    # Filtrar las categorías si se proporcionan los parámetros de filtro
    list_category = Category.objects.all()

    if category_name:
        list_category = list_category.filter(category_name=category_name)
    if category_id:  
        list_category = list_category.filter(id=category_id)

    if not list_category:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No hay datos registrados',
            'data': None
        }
        return Response(response_data)

    data = []

    for item in list_category:
        serializer_ctg = CategorySerializer(item)
        item_data = serializer_ctg.data
        data.append(item_data)

    response_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos encontrados',
        'data': data
    }
    return Response(response_data)

@api_view(['POST'])
def create_category(request):
    data = request.data

    # Obtener los datos de la categoría del JSON enviado en la solicitud
    category_name = data.get('category_name')
    description = data.get('description')

    # Verificar si los campos requeridos están vacíos
    empty_fields = []
    required_fields = ['category_name', 'description']
    for field in required_fields:
        if not data.get(field):
            empty_fields.append(field)

    if empty_fields:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Los siguientes campos no pueden estar vacíos: ' + ', '.join(empty_fields),
            'status': False
        }
        return Response(response_data)

    # Verificar si la descripción tiene más de 250 caracteres
    if len(description) > 250:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'La descripción no puede tener más de 250 caracteres.',
            'status': False
        }
        return Response(response_data)

    # Verificar si ya existe una categoría con el mismo nombre
    if Category.objects.filter(category_name=category_name).exists():
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': f'Ya existe una categoría con el nombre: {category_name}',
            'data': None
        }
        return Response(response_data)

    # Crear una instancia de Category utilizando los datos proporcionados
    category_data = {
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
            'data': None
        }
        return Response(response_data)
    else:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Error al crear la categoría',
            'data': category_create.errors
        }
        return Response(response_data)

@api_view(['PATCH'])
def update_category(request, pk):
    try: 
        update_category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Datos no encontrados',
            'data': None
        }
        return Response(responde_data)
    
    # Obtener los datos actualizados de la categoría del JSON enviado en la solicitud
    category_name = request.data.get('category_name')
    
    # Verificar si ya existe una categoría con el mismo nombre
    if Category.objects.exclude(pk=pk).filter(category_name=category_name).exists():
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': f'Ya existe una categoría con el nombre: {category_name}',
            'data': None
        }
        return Response(response_data)

    serializer_category = CategorySerializer(update_category, data=request.data, partial=True)
    serializer_category.is_valid(raise_exception=True)
    serializer_category.save()

    responde_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos de actualizados exitosamente',
        'data': None
    }
    return Response(responde_data)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        delete_category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Categoria no existe o ya fue eliminada',
            'data': None 
        }
        return Response(responde_data)
    
    category_name = delete_category.category_name
    delete_category.delete()

    response_data ={
        'code': status.HTTP_200_OK,
        'message': f'Datos de {category_name} eliminados exitosamente',
        'status': True,
        'data': None
    }
    
    return Response(response_data)

    

@api_view(['PATCH'])
def update_category(request, pk):
    try: 
        update_category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Datos no encontrados',
            'data': None
        }
        return Response(responde_data)
    
    # Obtener los datos actualizados de la categoría del JSON enviado en la solicitud
    category_name = request.data.get('category_name')
    
    # Verificar si ya existe una categoría con el mismo nombre
    if Category.objects.exclude(pk=pk).filter(category_name=category_name).exists():
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': f'Ya existe una categoría con el nombre: {category_name}',
            'data': None
        }
        return Response(response_data)

    serializer_category = CategorySerializer(update_category, data=request.data, partial=True)
    serializer_category.is_valid(raise_exception=True)
    serializer_category.save()

    responde_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos de actualizados exitosamente',
        'data': None
    }
    return Response(responde_data)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        delete_category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Categoria no existe o ya fue eliminada',
            'data': None 
        }
        return Response(responde_data)
    
    category_name = delete_category.category_name
    delete_category.delete()

    response_data ={
        'code': status.HTTP_200_OK,
        'message': f'Datos de {category_name} eliminados exitosamente',
        'status': True,
        'data': None
    }
    
    return Response(response_data)