from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #CATEGORY

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_category(request):
    queyset = Category.objects.all()
    serializer = CategorySerializer(queyset, many=True)
    return Response(serializer.data)
    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_category(request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)