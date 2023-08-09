import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_category(request):
        category_type = request.GET.get('category_type')
        sport_id = request.GET.get('sport')
        category_name = request.GET.get('category_name')

        # Filtrar las categorías si se proporcionan los parámetros de filtro
        list_category = Category.objects.all()

        if category_type:
            list_category = list_category.filter(category_type=category_type)
        if sport_id:
            list_category = list_category.filter(sport__id=sport_id)
        if category_name:
            list_category = list_category.filter(category_name=category_name)

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
            sport_id = serializer_ctg.data['sport']  # Remover el ID del deporte del objeto
            sport = Sports.objects.get(id=sport_id)
            item_data = serializer_ctg.data
            item_data['sport'] = f"{sport.sport_name } "# Añadir el nombre del deporte
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
    sport_id = data.get('sport')
    category_type = data.get('category_type')
    category_name = data.get('category_name')

    # Verificar si los campos requeridos están vacíos
    empty_fields = []
    required_fields = ['sport', 'category_type', 'category_name']
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

    # Crear una instancia de Sport basada en el ID proporcionado
    try:
        sport = Sports.objects.get(pk=sport_id)
    except Sports.DoesNotExist:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'El ID del deporte proporcionado no existe.',
            'status': False,
            'data': None
        }
        return Response(response_data)
     # Crear una instancia de Category utilizando los datos proporcionados
    category_data = {
        'sport': sport.pk,
        'category_type': category_type,
        'category_name': category_name
    }

    category_create = CategorySerializer(data=category_data)
    if category_create.is_valid():
        category_create.save()
        response_data = {
            'code': status.HTTP_201_CREATED,
            'status': True,
            'message': f'categoria {category_name} Creada exitosamente',
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
    
    serializer_category = CategorySerializer(update_category, data=request.data, partial=True)
    serializer_category.is_valid(raise_exception=True)
    serializer_category.save()

    responde_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos actualizados exitosamente',
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
            'message': 'Datos no encontrados',
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