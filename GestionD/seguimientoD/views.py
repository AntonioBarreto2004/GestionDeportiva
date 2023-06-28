from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from .models import *

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


    #ANTHROPOMETRIC

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



