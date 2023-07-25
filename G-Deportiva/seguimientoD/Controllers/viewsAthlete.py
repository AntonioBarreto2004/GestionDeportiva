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
    
    serializer = CategorySerializer(filtered_queryset, many=True)
    
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
    if serializer.is_valid(raise_exception=True):
        # Obtener los datos validados del serializador
        validated_data = serializer.validated_data
         # Filtrar los usuarios por rol "Atleta"
        athletes = User.objects.filter(cod_rol__name_rol='Atleta')
        # Asignar los usuarios filtrados al campo at_user del atleta
        validated_data['at_user'] = athletes

        # Obtener los valores de at_position y at_positiona del modelo Positions
        at_position_data = validated_data.get('c_position', {})
        at_positiona_data = validated_data.get('c_positiona', {})
        at_position_value = at_position_data.get('at_position', '')
        at_positiona_value = at_positiona_data.get('at_positiona', '')

        # Asignar los valores de at_position y at_positiona al atleta
        validated_data['at_position'] = at_position_value
        validated_data['at_positiona'] = at_positiona_value

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
    else:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Error al registrar el atleta',
            'status': False
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
    

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