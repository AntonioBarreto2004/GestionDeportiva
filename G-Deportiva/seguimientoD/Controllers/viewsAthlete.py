from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from ..serializer import *
from ..models import *

#ATHLETE

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete(request):
    class filter_athlete(filters.FilterSet):
        class Meta:
            Model = Athlete
            fields = {
                'id':['exact', 'icontains'],
                'a_category':['exact', 'icontains'],
                'at_team':['exact', 'icontains'],
                'c_position':['exact', 'icontains'],
                'c_positiona':['exact', 'icontains'],
            }

    queryset = Athlete.objects.all()
    athlete_filter = filter_athlete(request.query_params, queryset=queryset)
    filtered_queryset = athlete_filter.qs

    if not filtered_queryset.exists():
        return Response(
            data={'code': status.HTTP_404_NOT_FOUND, 
            'message': 'No hay datos registrados', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AthleteSerializer(filtered_queryset, many=True)
    
    responde_data={
        'code': status.HTTP_200_OK,
        'message': 'Lista de Atletas exitosa',
        'status' : True,
    }
    return Response(data=(responde_data, serializer.data), status=status.HTTP_200_OK)

    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_athlete(request):
    serializer = AthleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
        # Obtener el nombre del equipo de la solicitud
    at_user = serializer.validated_data['at_user']

    # Verificar si ya existe un equipo con el mismo nombre
    if Athlete.objects.filter(at_user=at_user).exists():
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Ya existe un Atleta Registrado',
            'status': False
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        response_data = {
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Debes iniciar sesión para crear un equipo.',
            'status': False
        }
        return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)

    # Verificar si el usuario existe y tiene el rol de "Instructor" o "Administrador"
    user = request.user
    try:
        if not user.cod_rol.name_rol in ['Instructor', 'Administrador']:
            response_data = {
                'code': status.HTTP_403_FORBIDDEN,
                'message': 'No tienes permisos para crear un equipo.',
                'status': False
            }
            return Response(data=response_data, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'El usuario no existe.',
            'status': False
        }
        return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    # Guardar el atleta
    serializer.save()

    response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Atleta registrado exitosamente',
            'status': True,
        }
    return Response(data=(response_data), status=status.HTTP_201_CREATED)
    

@api_view(['PATCH'])
def update_athlete(request, pk):
    try:
        athlete = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
         return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                               'message': 'Atleta no encontrado.', 
                               'status': False}, 
                               status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
    
    serializer = AthleteSerializer(athlete, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response_data ={
        'code': status.HTTP_200_OK,
        'message': f'Datos de {athlete.at_user.name} actualizados exitosamente',
        'status': True
    }
    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_athlete(request, pk):
    try:
        athlete = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Atleta no encontrado.', 
                              'status': False}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

    athlete_name = athlete.at_user.name
    athlete.delete()
    
    response_data ={
        'code': status.HTTP_204_NO_CONTENT,
        'message': f'Datos de {athlete_name} eliminados exitosamente',
        'status': True
    }
    return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)