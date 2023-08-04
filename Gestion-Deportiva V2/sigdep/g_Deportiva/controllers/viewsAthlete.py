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
    class filter_athlete(filters.FilterSet):
        class Meta:
            model = Athlete
            fields = {
                'id': ['exact'],
                'instructor': ['exact'],
                'technicalv': ['exact'],
                'tacticalv': ['exact'],
                'physicalv': ['exact'],
                'sports': ['exact'],
                'athlete_status': ['exact'],
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
            }
        )
    serializer = AthleteSerializer(filtered_queryset, many=True)

    data = []
    for item in serializer.data:
        instructor_id = item.pop('instructor')  # Remover el ID del instructor del objeto
        instructor = Instructors.objects.get(id=instructor_id)
        item['instructor'] = f"{instructor.people.name} {instructor.people.last_name}"  # Añadir el nombre del instructor

        person_id = item.pop('people')  # Remover el ID de la persona del objeto
        person = People.objects.get(id=person_id)
        item['person'] = f"{person.name} {person.last_name}"  # Añadir el nombre de la persona

        sport_id = item.pop('sports')  # Remover el ID del deporte del objeto
        sport = Sports.objects.get(id=sport_id)
        item['sport'] = sport.sport_name  # Añadir el nombre del deporte

        data.append(item)

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Lista de Atletas exitosa',
        'status': True,
        'data': data
    }
    return Response(response_data)


    
@api_view(['POST'])
def create_athlete(request):
    person_id = request.data.get('people')

    if Athlete.objects.filter(people_id=person_id).exists():
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Ya existe un Atleta asociado a esta persona.',
            'status': False,
            'data': None
        }
        return Response(response_data)
    
    try:
        person = People.objects.get(id=person_id)
        user = User.objects.get(people=person)
        print("Rol del usuario:", user.rol)
        if user.rol.name_rol != "Atleta":
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'La persona no tiene el rol de Atleta.',
                    'data': None
                }
            )
    except People.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_400_BAD_REQUEST,
                'status': False,
                'message': 'La persona no existe.',
                'data': None
            }
        )
    
    instructor_id = request.data.get('instructor')
    if not instructor_id:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'El campo instructor es requerido.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        instructor = Instructors.objects.get(id=instructor_id)
    except Instructors.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'Instructor no encontrado.',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AthleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(instructor=instructor)  # Establecer el objeto instructor en lugar del ID

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