import re
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *

 #TEAM

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_team(request):
    try:
        team_name = request.GET.get('team_name', '')
        team_category_id = request.GET.get('team_category_id', '')

        queryset = Team.objects.all()

        if team_name:
            queryset = queryset.filter(team_name__icontains=team_name)

        if team_category_id:
            queryset = queryset.filter(team_category_id=team_category_id)

        if not queryset.exists():
            return Response(
                data={'code': status.HTTP_200_OK, 
                    'message': 'No hay datos registrados', 
                    'status': False,
                    'data': None
                    }
            )

        serializer = TeamSerializer(queryset, many=True)

        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Lista de equipos exitosa',
            'status': True,
            'data' : serializer.data
        }

        return Response(response_data)
    
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL fallo. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)

    
    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_team(request):
    try:
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        person_id = request.data.get('instructors')
        team_name = serializer.validated_data['team_name']
        description = serializer.validated_data['description']

        # Validating the name field
        if not team_name:
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Nombre del deporte no puede estar vacío.',
                'status': False,
                'data': None
            })

        if not re.match(r'^[a-zA-Z\s]+$', team_name):
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Nombre del Equipo solo puede contener letras y espacios.',
                'status': False,
                'data': None
            })

        # Validating the description field
        if len(description) > 250:
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'La descripción no puede exceder los 250 caracteres.',
                'status': False,
                'data': None
            })

        # Verificar si ya existe un equipo con el mismo nombre
        if Team.objects.filter(team_name=team_name).exists():
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Ya existe un equipo con el mismo nombre.',
                'status': False,
                'data': None
            }
            return Response(response_data)
        
        user = User.objects.get(instructors=person_id)
        if user.rol_id != 2:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'La persona no tiene el rol de instructor.',
                    'data': None
                })


        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Debes iniciar sesión para crear un equipo.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        # Verificar si el usuario existe y tiene el rol de "Instructor" o "Administrador"
        user = request.user
        try:
            if not user.cod_rol.name in ['Instructor', 'Administrador']:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'No tienes permisos para crear un equipo.',
                    'status': False,
                    'data': None
                }
                return Response(response_data)
        except User.DoesNotExist:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El usuario no existe.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        serializer.save()

        response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Equipo creado exitosamente',
            'status': True,
            'data':None
        }
        return Response(response_data)
    
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)



    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_team(request, pk):
    try:
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'Equipo no existente',
                'status': False,
                'data': None
            }
            return Response(responde_data)
        
        team_name = request.data.get('team_name')

        existing_sport = Sports.objects.filter(team_name=team_name).first()
        if existing_sport:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'Ya existe un Equipo con el mismo nombre.',
                    'data': None
                })

        serializer = TeamSerializer(team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data ={
            'code': status.HTTP_200_OK,
            'message': 'Equipo actualizado exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data)
    
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)


    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_team(request, pk):
    try:
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'Equipo no existente',
                'status': False,
                'data': None
            }
            return Response(responde_data)

        team_name = team.team_name
        team.delete()
        responde_data = {
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Equipo {team_name} Eliminada Exitosamente',
            'status': True,
            'data': None
        }
        return Response(data=responde_data,status=status.HTTP_204_NO_CONTENT)
    
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)