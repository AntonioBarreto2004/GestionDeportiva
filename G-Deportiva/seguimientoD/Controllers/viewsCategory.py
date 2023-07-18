from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #CATEGORY

     #METODO GET (LISTAR)
@api_view(['GET'])
def list_category(request):
    class CategoryFilter(filters.FilterSet):
        class Meta:
            model = Category
            fields = {
            'id': ['exact', 'icontains'],
            't_name': ['exact', 'icontains'],
            'c_name': ['exact', 'icontains'],
        }
    queryset = Category.objects.all()
    category_filter = CategoryFilter(request.query_params, queryset=queryset)
    filtered_queryset = category_filter.qs

    if not filtered_queryset.exists():
        return Response(
            data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No hay datos registrados', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CategorySerializer(filtered_queryset, many=True)
    responde_data={
        'code': status.HTTP_200_OK,
        'message': 'Lista de Categorias exitosa',
        'status' : True,
    }
    return Response(data=(responde_data, serializer.data), status=status.HTTP_200_OK)

    
    #METODO POST (AGREGAR)

@api_view(['POST'])
def create_category(request):
    serializerC = CategorySerializer(data=request.data)
    serializerC.is_valid(raise_exception=True)
    validated_data = serializerC.validated_data

    t_name = validated_data.get('t_name', '')
    c_name = validated_data.get('c_name', '')

    # Validación adicional
    if Category.objects.filter(t_name=t_name).exists():
        return Response(
            data={'code': status.HTTP_409_CONFLICT, 'message': 'Los datos ya existen', 'status': False},
            status=status.HTTP_409_CONFLICT
        )

    with transaction.atomic():
        try:
            serializerC.save()
        except Exception as e:
            return Response(
                data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error al crear la categoría', 'status': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Devolver datos completos de la categoría creada
        response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Categoría creada exitosamente',
            'status': True
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(data={'code': '404_NOT_FOUND', 
                              'message': 'Categoría no encontrada.', 
                              'status': False}, 
                              status=status.HTTP_404_NOT_FOUND
                        )
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response_data ={
        'code': status.HTTP_200_OK,
        'message': 'Categoría actualizada exitosamente',
        'status': True
    }
    
    return Response(data=response_data, status=status.HTTP_200_OK)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        responde_data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Categoria no existente',
            'status': False
        }
        return Response(data={responde_data},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    name_category = category.t_name
    category.delete()
    responde_data = {
        'code': status.HTTP_204_NO_CONTENT,
        'message': f'Categoria {name_category} Eliminada Exitosamente',
        'status': True
    }
    return Response(data=responde_data,status=status.HTTP_204_NO_CONTENT)