from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

 #TEAM

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_team(request):
    team_name = request.GET.get('team_name', '')
    team_category_id = request.GET.get('team_category_id', '')

    queryset = Team.objects.all()

    if team_name:
        queryset = queryset.filter(team_name__icontains=team_name)

    if team_category_id:
        queryset = queryset.filter(team_category_id=team_category_id)

    if not queryset.exists():
        return Response(
            data={'code': status.HTTP_404_NOT_FOUND, 
                  'message': 'No hay datos registrados', 
                  'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TeamSerializer(queryset, many=True)

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Lista de equipos exitosa',
        'status': True,
    }

    return Response(data=(response_data, serializer.data), status=status.HTTP_200_OK)

    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Obtener el nombre del equipo de la solicitud
    team_name = serializer.validated_data['team_name']

    # Verificar si ya existe un equipo con el mismo nombre
    if Team.objects.filter(team_name=team_name).exists():
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Ya existe un equipo con el mismo nombre.',
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

    serializer.save()

    response_data = {
        'code': status.HTTP_201_CREATED,
        'message': 'Equipo creado exitosamente',
        'status': True
    }
    return Response(data=response_data, status=status.HTTP_201_CREATED)



    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
         responde_data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Categoria no existente',
            'status': False
        }
         return Response(data=responde_data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = TeamSerializer(team, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    response_data ={
        'code': status.HTTP_200_OK,
        'message': 'Equipo actualizado exitosamente',
        'status': True
    }
    return Response(data=response_data, status=status.HTTP_200_OK)


    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        responde_data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Categoria no existente',
            'status': False
        }
        return Response(data=responde_data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    team_name = team.team_name
    team.delete()
    responde_data = {
        'code': status.HTTP_204_NO_CONTENT,
        'message': f'Equipo {team_name} Eliminada Exitosamente',
        'status': True
    }
    return Response(data=responde_data,status=status.HTTP_204_NO_CONTENT)