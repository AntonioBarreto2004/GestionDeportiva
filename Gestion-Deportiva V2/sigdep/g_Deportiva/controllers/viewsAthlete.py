import requests
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from ..serializers import *
from ..models import *

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
def create_athlete(request):
    serializer = AthleteSerializer(data=request.data)
    if serializer.is_valid():
        # Obtener el ID de la persona del atleta y el instructor de la solicitud
        person_id = request.data.get('people')

        # Verificar si ya existe un atleta con la misma persona asociada
        if Athlete.objects.filter(people_id=person_id).exists():
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Ya existe un Atleta asociado a esta persona.',
                'status': False,
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si la persona tiene el rol de Atleta (rol=3)
        try:
            person = People.objects.get(id=person_id)
            user = User.objects.get(people=person)
            if user.rol_id != 1:  # Asumiendo que el rol de Atleta tiene id=3, ajusta esto si es necesario
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'status': False,
                    'message': 'La persona no es Atleta.',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        except People.DoesNotExist:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'status': False,
                'message': 'La persona no existe.',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Guardar el atleta
        serializer.save()

        return Response({
            'code': status.HTTP_201_CREATED,
            'message': 'Atleta registrado exitosamente',
            'status': True,
            'data': None
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

    

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