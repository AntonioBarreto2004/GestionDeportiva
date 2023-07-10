from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

#ATHLETE

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete(request):
    queyset = Athlete.objects.all()
    serializer = AthleteSerializer(queyset, many=True)
    return Response(serializer.data)
    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_athlete(request):
        serializer = AthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_athlete(request, pk):
    try:
        athlete = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = AthleteSerializer(athlete, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_athlete(request, pk):
    try:
        athlete = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    athlete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)