from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

#METODO GET (LISTAR)
@api_view(['GET'])
def list_anthro(request):
    queyset = Anthropometric.objects.all()
    serializer = AnthropometricSerializer(queyset, many=True)
    return Response(serializer.data)
    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_anthro(request):
        serializer = AnthropometricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_anthro(request, pk):
    try:
        anthrop = Anthropometric.objects.get(pk=pk)
    except Anthropometric.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = AnthropometricSerializer(anthrop, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_anthro(request, pk):
    try:
        anthrop = Anthropometric.objects.get(pk=pk)
    except Anthropometric.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    anthrop.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)  


