import requests
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #POSITIONS

    #METODO GET (LISTAR)
@api_view(['GET'])
def list_positions(request):
    try:
        class PositionsFilter(filters.FilterSet):
            class Meta:
                model = Positions
                fields = {
                    'p_category': ['exact'],
                    'at_position': ['exact', 'icontains'],
                    'at_positiona': ['exact', 'icontains'],
                }

        queryset = Positions.objects.all()
        positions_filter = PositionsFilter(request.query_params, queryset=queryset)
        filtered_queryset = positions_filter.qs

        if not filtered_queryset.exists():
            return Response(
                data={'code': status.HTTP_200_OK, 'message': 'No hay datos registrados', 'status': False, 'data': None},
            )

        serializer = PositionsSerializer(filtered_queryset, many=True)

        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Lista de posiciones exitosa',
            'status': True,
            'data': serializer.data
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

    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_positions(request):
    try:
        serializer = PositionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener los datos validados del serializador
        validated_data = serializer.validated_data

        # Obtener la categoría y las posiciones principales y alternativas de la solicitud
        category = validated_data.get('p_category')
        at_position = validated_data.get('at_position')
        at_positiona = validated_data.get('at_positiona')

        # Verificar si las posiciones ya existen para la categoría seleccionada
        if Positions.objects.filter(p_category=category, at_position=at_position).exists() or Positions.objects.filter(p_category=category, at_positiona=at_positiona).exists():
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Las posiciones ya existen para esta categoría',
                'state': False,
                'data': None
            }
            return Response(response_data)

        # Guardar la posición
        serializer.save()
        response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Posición creada exitosamente',
            'state': True,
            'data':None
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
def update_positions(request, pk):
    try:
        try:
            position = Positions.objects.get(pk=pk)
        except Positions.DoesNotExist:
            return Response(
                data={'code': status.HTTP_200_OK, 'message': 'La posición no existe', 'status': False, 'data':None},
            )

        serializer = PositionsSerializer(position, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'code': status.HTTP_200_OK,
            'message': f'Posición actualizada exitosamente',
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


@api_view(['DELETE'])
def delete_positions(request, pk):
    try:
        try:
            position = Positions.objects.get(pk=pk)
        except Positions.DoesNotExist:
            return Response(
                data={'code': status.HTTP_200_OK, 
                    'message': 'La posición no existe', 
                    'status': False,
                    'data':None
                    },
            )

        position_name = position.at_position  # Obtener el nombre de la posición antes de eliminarla
        position.delete()

        response_data = {
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Posición "{position_name}" eliminada exitosamente',
            'status': True,
            'data':None,
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
