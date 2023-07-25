from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sports
from django_filters import rest_framework as filters
from ..serializer import SportsSerializer
from django.db import IntegrityError

@api_view(['GET'])
def list_sports(request):
    class sportsFilter(filters.FilterSet):
        class Meta:
            model = Sports
            fields = {
            'id': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'creation_date': ['exact', 'year__gt', 'year__lt'],
        }

    queryset = Sports.objects.all()
    sports_filter = sportsFilter(request.query_params, queryset=queryset)
    filtered_queryset = sports_filter.qs

    if not filtered_queryset.exists():
        return Response(
            data={'code': '404_NOT_FOUND', 'message': 'Error al encontrar datos', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = SportsSerializer(filtered_queryset, many=True)
    response_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos Encontrados',
        'data': serializer.data
    }
    return Response(response_data)

@api_view(['POST'])
def create_sports(request):
    serializer = SportsSerializer(data=request.data)
    if serializer.is_valid():
        # Verificar si ya existe un deporte con el mismo nombre (o campo único) en la base de datos
        name = serializer.validated_data['name']
        try:
            existing_sport = Sports.objects.get(name=name)
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': f'El deporte "{name}" ya existe',
                'status': False
            }
            return Response(data=responde_data)
        except Sports.DoesNotExist:
            # Si el deporte no existe, guardar el objeto de deporte en la base de datos
            serializer.save()
            responde_data = {
                'code': status.HTTP_201_CREATED,
                'message': 'Deporte creado exitosamente',
                'status': True,
                'data': None
            }
            return Response(responde_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def sports_detail(request, pk):
    try:
        sports = Sports.objects.get(pk=pk)
    except Sports.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK,
                  'message': 'El deporte no existe o ya fue eliminado',
                  'status': False,
                  'data': None
                  }
        )

    if request.method == 'GET':
        serializer = SportsSerializer(sports)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SportsSerializer(sports, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sports.delete()
        responde_data={
            'code':status.HTTP_204_NO_CONTENT,
            'message':'Deporte eliminado correctamente',
            'status':True,
            'data': None
        }
        return Response(responde_data)