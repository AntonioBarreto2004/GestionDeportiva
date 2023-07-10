from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #POSITIONS

    #METODO GET (LISTAR)
@api_view(['GET'])
def list_positions(request):
    queyset = Positions.objects.all()
    serializer = PositionsSerializer(queyset, many=True)
    return Response(serializer.data)
    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_positions(request):
        serializer = PositionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'message': 'Posición creada exitosamente'}, status=status.HTTP_201_CREATED, )

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_positions(request, pk):
    try:
        position = Positions.objects.get(pk=pk)
    except Positions.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = PositionsSerializer(position, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_positions(request, pk):
    try:
        position = Positions.objects.get(pk=pk)
    except Positions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    position.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
