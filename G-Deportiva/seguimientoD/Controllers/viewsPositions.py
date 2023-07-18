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
            data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No hay datos registrados', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PositionsSerializer(filtered_queryset, many=True)

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Lista de posiciones exitosa',
        'status': True,
    }

    return Response(data=(response_data, serializer.data), status=status.HTTP_200_OK)

    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_positions(request):
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
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Las posiciones ya existen para esta categoría',
            'state': False
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    # Guardar la posición
    serializer.save()
    response_data = {
        'code': status.HTTP_201_CREATED,
        'message': 'Posición creada exitosamente',
        'state': True
    }
    return Response(data=response_data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_positions(request, pk):
    try:
        position = Positions.objects.get(pk=pk)
    except Positions.DoesNotExist:
        return Response(
            data={'code': status.HTTP_404_NOT_FOUND, 'message': 'La posición no existe', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PositionsSerializer(position, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    response_data = {
        'code': status.HTTP_200_OK,
        'message': f'Posición actualizada exitosamente',
        'status': True,
    }

    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_positions(request, pk):
    try:
        position = Positions.objects.get(pk=pk)
    except Positions.DoesNotExist:
        return Response(
            data={'code': status.HTTP_404_NOT_FOUND, 
                'message': 'La posición no existe', 
                'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    position_name = position.at_position  # Obtener el nombre de la posición antes de eliminarla
    position.delete()

    response_data = {
        'code': status.HTTP_204_NO_CONTENT,
        'message': f'Posición "{position_name}" eliminada exitosamente',
        'status': True,
    }

    return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
