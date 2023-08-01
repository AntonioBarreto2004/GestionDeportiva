import requests
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from ..serializers import AthleteSerializer
from ..models import Athlete, People
from django.contrib.auth.models import User


# Clase FilterAthlete para filtrar los datos de los atletas
class FilterAthlete(filters.FilterSet):
    class Meta:
        model = Athlete
        fields = {
            'id': ['exact'],
            'instructor': ['exact'],
            'people': ['exact'],
            'sports': ['exact'],
        }


# METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete(request):
    try:
        queryset = Athlete.objects.all()
        athlete_filter = FilterAthlete(request.query_params, queryset=queryset)
        filtered_queryset = athlete_filter.qs

        if not filtered_queryset.exists():
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'No hay datos registrados',
                    'status': False,
                    'data': None
                },
            )

        serializer = AthleteSerializer(filtered_queryset, many=True)

        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Lista de Atletas exitosa',
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
def create_athlete(request):
    try:
        serializer = AthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener el ID del usuario del campo 'at_user'
        user_id = request.data.get('id')

        # Verificar si el usuario existe en la base de datos
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El usuario no existe.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Debes iniciar sesión para crear un atleta.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        # Verificar si el usuario existe y tiene el rol de "Instructor" o "Administrador"
        try:
            if not user.rol.name_rol in ['Instructor', 'Administrador']:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'No tienes permisos para crear un atleta.',
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

        # Guardar el atleta
        serializer.save()

        response_data = {
            'code': status.HTTP_201_CREATED,
            'message': 'Atleta registrado exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

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


# METODO PUT/PATCH (ACTUALIZAR)
@api_view(['PUT', 'PATCH'])
def update_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Atleta no encontrado.',
                    'status': False,
                    'data': None
                }
            )

        serializer = AthleteSerializer(athlete, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'code': status.HTTP_200_OK,
            'message': f'Datos de {athlete.instructor.name} actualizados exitosamente',
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


# METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Atleta no encontrado.',
                    'status': False,
                    'data': None
                }
            )

        athlete_name = athlete.instructor.name
        athlete.delete()

        response_data = {
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Datos de {athlete_name} eliminados exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

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
