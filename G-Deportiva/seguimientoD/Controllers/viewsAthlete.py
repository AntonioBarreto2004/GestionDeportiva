import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import AuthenticationFailed  # esta es la línea corregida
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import status
from ..serializer import *
from ..models import *


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            raise AuthenticationFailed('Tu token es inválido o ha expirado.')

        return self.get_user(validated_token), validated_token


#ATHLETE

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete(request):
    try:
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
                data={
                    'code': status.HTTP_200_OK, 
                    'message': 'No hay datos registrados',
                    'status': False,
                    'data': None
                    },
            )
        
        serializer = AthleteSerializer(filtered_queryset, many=True)
        
        responde_data={
            'code': status.HTTP_200_OK,
            'message': 'Lista de Atletas exitosa',
            'status' : True,
            'data': serializer.data
        }
        return Response(responde_data)
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

    
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create_athlete(request):
        data=request.data
        required_fields=["a_category", "at_team", "c_position", "c_positiona"]

        missing_fields=[field for field in required_fields if field not in data]
        if missing_fields:
            data={
                'code': status.HTTP_400_BAD_REQUEST ,
                'status': False, 
                'message': f"Los siguientes campos son requeridos: {', '.join(missing_fields)}",
                'data': None 
            }
            return Response(data)

        from django.core.exceptions import ObjectDoesNotExist


        serializer = AthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        at_user = serializer.validated_data['at_user']

        if Athlete.objects.filter(at_user=at_user).exists():
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Ya existe un Atleta Registrado',
                'status': False,
                'data': None
            }
            return Response(response_data)

        if not request.user.is_authenticated:
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Debes iniciar sesión para crear un equipo.',
                'status': False,
                'data': None
            }
            return Response(response_data)

        user = request.user
        try:
            if not user.cod_rol.name_rol in ['Instructor', 'Administrador']:
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
            'message': 'Atleta registrado exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data)
    

    

@api_view(['PATCH'])
def update_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Atleta no encontrado.', 
                                'status': False,
                                'data':None
                                },
                            )
        
        serializer = AthleteSerializer(athlete, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_data ={
            'code': status.HTTP_200_OK,
            'message': f'Datos de {athlete.at_user.name} actualizados exitosamente',
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


@api_view(['DELETE'])
def delete_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Atleta no encontrado.', 
                                'status': False,
                                'data':None
                                }, 
                    
                            )

        athlete_name = athlete.at_user.name
        athlete.delete()
        
        response_data ={
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Datos de {athlete_name} eliminados exitosamente',
            'status': True,
            'data': None
        }
        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
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