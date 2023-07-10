from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #TEAM

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_team(request):
    queyset = Team.objects.all()
    serializer = TeamSerializer(queyset, many=True)
    return Response(serializer.data)
    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_team(request):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TeamSerializer(team, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    team.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)