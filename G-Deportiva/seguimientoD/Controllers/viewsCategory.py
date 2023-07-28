import requests
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
    try:
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
            respuesta = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'No hay datos registrados',
                'data': None
            }
            return Response(respuesta)
        
        serializer = CategorySerializer(filtered_queryset, many=True)
        responde_data={
            'code': status.HTTP_200_OK,
            'message': 'Lista de Categorias exitosa',
            'status' : True,
            'data': serializer.data
        }
        return Response(responde_data)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)

    
    #METODO POST (AGREGAR)

@api_view(['POST'])
def create_category(request):
    try:
        serializerC = CategorySerializer(data=request.data)
        serializerC.is_valid(raise_exception=True)
        validated_data = serializerC.validated_data

        t_name = validated_data.get('t_name', '')
        c_name = validated_data.get('c_name', '')

        # Validación adicional
        if Category.objects.filter(t_name=t_name).exists():
            data={'code': status.HTTP_200_OK, 
                    'status': False,
                    'message': 'Los datos ya existen', 
                    'data': None
                    }
            return Response(data)

        with transaction.atomic():
            try:
                serializerC.save()
            except Exception as e:
                return Response(
                    data={'code': status.HTTP_200_OK, 'message': 'Error al crear la categoría', 'status': False,'data': None},
                    
                )

            # Devolver datos completos de la categoría creada
            response_data = {
                'code': status.HTTP_201_CREATED,
                'message': 'Categoría creada exitosamente',
                'status': True,
                'data': None
            }
            return Response(response_data)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)

@api_view(['PATCH'])
def update_category(request, pk):
    try:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Categoría no encontrada.', 
                                'status': False,
                                'data': None
                                }, 
                            )
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_data ={
            'code': status.HTTP_200_OK,
            'message': 'Categoría actualizada exitosamente',
            'status': True,
            'data': None
        }
        
        return Response(response_data)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'Categoria no existente',
                'status': False,
                'data': None
            }
            return Response(responde_data)

        name_category = category.t_name
        category.delete()
        responde_data = {
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Categoria {name_category} Eliminada Exitosamente',
            'status': True,
            'data':None
        }
        return Response(responde_data)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)