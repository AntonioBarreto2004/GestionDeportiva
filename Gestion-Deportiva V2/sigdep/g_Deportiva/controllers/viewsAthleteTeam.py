# views.py
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from ..serializers import AthleteTeamSerializer
from ..models import AthleteTeam
from django.contrib.auth.models import User

# METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete_team(request):
    try:
        class FilterAthleteTeam(filters.FilterSet):
            class Meta:
                model = AthleteTeam
                fields = {
                    'id': ['exact', 'icontains'],
                    'athlete': ['exact', 'icontains'],
                    'team': ['exact', 'icontains'],
                }

        queryset = AthleteTeam.objects.all()
        athlete_team_filter = FilterAthleteTeam(request.query_params, queryset=queryset)
        filtered_queryset = athlete_team_filter.qs

        if not filtered_queryset.exists():
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'No hay datos registrados',
                    'status': False,
                    'data': None
                },
            )

        serializer = AthleteTeamSerializer(filtered_queryset, many=True)

        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Lista de Atletas de Equipos exitosa',
            'status': True,
            'data': serializer.data
        }
        return Response(response_data)
    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)

# METODO POST (AGREGAR)
@api_view(['POST'])
def create_athlete_team(request):
    try:
        serializer = AthleteTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el atleta y el equipo ya están asociados en la tabla AthleteTeam
        athlete = serializer.validated_data['athlete']
        team = serializer.validated_data['team']

        if AthleteTeam.objects.filter(athlete=athlete, team=team).exists():
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El atleta ya está asociado a este equipo.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Debes iniciar sesión para crear una asociación de atleta y equipo.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        # Verificar si el usuario existe y tiene el rol de "Instructor" o "Administrador"
        user = request.user
        try:
            if not user.cod_rol.name_rol in ['Instructor', 'Administrador']:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'No tienes permisos para crear una asociación de atleta y equipo.',
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

        # Guardar la asociación de atleta y equipo
        serializer.save()

        response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Asociación de Atleta y Equipo creada exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data)

    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)

@api_view(['PATCH'])
def update_athlete_team(request, pk):
    try:
        try:
            athlete_team = AthleteTeam.objects.get(pk=pk)
        except AthleteTeam.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK,
                                  'message': 'Asociación de Atleta y Equipo no encontrada.',
                                  'status': False,
                                  'data': None
                                  },
                            )

        serializer = AthleteTeamSerializer(athlete_team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'code': status.HTTP_200_OK,
            'message': f'Información de la Asociación de Atleta y Equipo actualizada exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data)
    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)

@api_view(['DELETE'])
def delete_athlete_team(request, pk):
    try:
        try:
            athlete_team = AthleteTeam.objects.get(pk=pk)
        except AthleteTeam.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK,
                                  'message': 'Asociación de Atleta y Equipo no encontrada.',
                                  'status': False,
                                  'data': None
                                  },
                            )

        athlete_team.delete()

        response_data = {
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'Asociación de Atleta y Equipo eliminada exitosamente',
            'status': True,
            'data': None
        }
        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)

